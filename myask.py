# --------------- Helpers that build all of the responses ----------------------
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
