"""
FizzBuzzゲームスキル
"""

import random

# --------------- Helpers that build all of the responses ----------------------
# TODO コードを分ける

def build_speechlet_response(card, output, reprompt_text, should_end_session):
    speech_dict = {'shouldEndSession': should_end_session}
    
    speech_dict['outputSpeech'] = {
        'type': 'SSML',
        'ssml': '<speak> ' + output + ' </speak>'
    }
    
    if card != None:
        speech_dict['card'] = {
            'type': 'Simple',
            'title': card['title'],
            'content': card['output']
        }
            
    if reprompt_text != None:
        speech_dict['reprompt'] = {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak> ' + reprompt_text + ' </speak>'
            }
        }
        
    return speech_dict


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict):
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_dict, speech_output, reprompt_text, should_end_session
    ))

def alexa_emit_tel(session_attributes, speech_output, card_dict):
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_dict, speech_output, None, should_end_session
    ))
    

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ 起動後のメッセージ
    """
    
    card_dict = {}
    session_attributes = {}
    
    # 応答text
    speech_output = "フィズバズゲームスキルへようこそ。" \
                    "このスキルでは、Fizz-Buzzゲームで私と対戦することができます。" \
                    "試しに、「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、" \
                    "のように話しかけてみてください。"
    # 8秒間発話がなかった場合に聞き返すためのtext 
    reprompt_text = "試しに、「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、" \
                    "のように話しかけてみてください。"

    # カード情報
    card_dict['title'] = "ようこそ"
    card_dict['output'] = speech_output

    return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)

# AMAZON.HelpIntent
def get_help_response():
    """ ヘルプメッセージ
    """

    card_dict = {}
    session_attributes = {}
    
    # 応答text
    speech_output = "Fizz-Buzzゲームをします。一から順に数字を読み上げ、その数字が三で割り切れるときはFizz、" \
                    "五で割り切れるときはBuzz、三と五の両方で割り切れるときはFizz-Buzzを数字の代わりに言ってください。" \
                    "間違ったり詰まったりしたら負けです。私かあなたのどちらからスタートするかは私が決めます。" \
                    "「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、のように話しかけてみてください。"
    # 8秒間発話がなかった場合に聞き返すためのtext 
    reprompt_text = '機能を使うために、「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、' \
                    'のように話しかけてみてください。'

    # カード情報
    card_dict['title'] = "機能説明"
    card_dict['output'] = speech_output
        
    return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)

# AMAZON.CancelIntent, AMAZON.StopIntent
def handle_session_end_request():
    """ 終了メッセージ
    """

    card_dict = {}
    session_attributes = {}

    # 応答text
    speech_output = 'またお会いしましょう。'
    
    # カード情報
    card_dict['title'] = 'さようなら'
    card_dict['output'] = speech_output

    return alexa_emit_tel(session_attributes, speech_output, card_dict)

## Custom Intent

## intentFbStartGame
def intent_fb_start_game(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    print('request {intent}'.format(intent=intent['name']))
    
    card_dict = {}
    session_attributes = {}
    
    if random.randint(0, 1) == 0:
        print('Alexaからスタート')
        speech_output = '私からスタートします。一'
        session_attributes['current_num'] = 2
        card_dict['output'] = '私からスタート：1'
    else:
        print('ユーザーからスタート')
        speech_output = 'あなたからどうぞ'
        session_attributes['current_num'] = 1
        card_dict['output'] = 'あなたからスタート'
    
    reprompt_text = 'あなたの番ですよ'

    # カード情報
    card_dict['title'] = 'ゲーム開始'
            
    return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)

## intentFbNumFizzBuzz
def intent_fb_num_fizz_buzz(intent, session):
    card_dict = {}
    session_attributes = {}
    has_num = False
    intent_num = 0
    has_fb = False
    intent_fb = ''
    
    if 'attributes' in session:
        current_num = int(session['attributes']['current_num'])

        if 'slots' in intent:
            if 'num' in intent['slots']:
                if 'value' in intent['slots']['num']:
                    has_num = True
                    if intent['slots']['num']['value'] == '?':
                        has_num = False
                    else:
                        intent_num = int(intent['slots']['num']['value'])
            
            if 'fb' in intent['slots']:
                if 'value' in intent['slots']['fb']:
                    has_fb = True
                    if intent['slots']['fb']['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == 'ER_SUCCESS_NO_MATCH':
                        has_fb = False
                    else:
                        intent_fb = intent['slots']['fb']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

        print(intent_fb)

        print(session['attributes']['current_num'])

        if has_num == False and has_fb == False:
            speech_output = 'うまく聞き取れませんでした。もう一度お願いします。'
            reprompt_text = 'もう一度、数字かFizz-Buzzを言ってください。'
            session_attributes['current_num'] = current_num
            card_dict['title'] = '！？'
            card_dict['output'] = 'うまく聞き取れませんでした。もう一度お願いします。'
            return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)

        if current_num % 3 == 0 and current_num % 5 == 0:
            # Fizz-Buzz
            if has_num:
                speech_output = '{num}ではなく、Fizz-Buzzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(num=intent_num)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Fizz-Buzzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
            elif intent_fb != 'Fizz-Buzz':
                speech_output = '{intent_fb}ではなく、Fizz-Buzzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(intent_fb=intent_fb)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Fizz-Buzzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
        elif current_num % 3 == 0:
            # Fizz
            if has_num:
                speech_output = '{num}ではなく、Fizzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(num=intent_num)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Fizzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
            elif intent_fb != 'Fizz':
                speech_output = '{intent_fb}ではなく、Fizzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(intent_fb=intent_fb)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Fizzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
        elif current_num % 5 == 0:
            # Buzz
            if has_num:
                speech_output = '{num}ではなく、Buzzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(num=intent_num)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Buzzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
            elif intent_fb != 'Buzz':
                speech_output = '{intent_fb}ではなく、Buzzが正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(intent_fb=intent_fb)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、Buzzです。'
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
        else:
            # number
            if has_fb:
                speech_output = '{intent_fb}ではなく、{num}が正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(intent_fb=intent_fb, num=current_num)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、{num}です。'.format(num=current_num)
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
            elif intent_num != current_num:
                speech_output = '{num_w}ではなく、{num_c}が正解です。残念ながら私の勝ちです。またお相手してくださいね。'.format(num_w=intent_num, num_c=current_num)
                card_dict['title'] = '不正解です'
                card_dict['output'] = '正解は、{num}です。'.format(num=current_num)
                return alexa_emit_tel(session_attributes, speech_output, card_dict)
                
        current_num += 1

        if current_num % 3 == 0 and current_num % 5 == 0:
            # Fizz-Buzz
            speech_output = 'Fizz-Buzz'
            card_dict['output'] = '私の答え: Fizz-Buzz'
        elif current_num % 3 == 0:
            # Fizz
            speech_output = 'Fizz'
            card_dict['output'] = '私の答え: Fizz'
        elif current_num % 5 == 0:
            # Buzz
            speech_output = 'Buzz'
            card_dict['output'] = '私の答え: Buzz'
        else:
            # number
            speech_output = '{num}'.format(num=current_num)
            card_dict['output'] = '私の答え: {num}'.format(num=current_num)
        session_attributes['current_num'] = current_num + 1
        reprompt_text = 'あなたの番ですよ'
        card_dict['title'] = 'Fizz-Buzz'

        return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)
    else:
        speech_output = 'まだゲームがスタートしていません。ゲームを開始するために' \
                        '「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、' \
                        'のように話しかけてみてください。'
        reprompt_text = '機能を使うために、「ゲームスタート」、や、「Fizz-Buzzゲームをしよう」、' \
                        'のように話しかけてみてください。'
        card_dict['title'] = 'エラー'
        card_dict['output'] = 'ゲームがまだスタートしていません。'
            
        return alexa_emit_ask(session_attributes, speech_output, reprompt_text, card_dict)


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "intentFbStartGame":
        return intent_fb_start_game(intent, session)
    elif intent_name == "intentFbNumFizzBuzz":
        return intent_fb_num_fizz_buzz(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent: " + intent_name)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

    
# --------------- Main handler ------------------

# lambdaに登録するハンドラ(Entry point)
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
