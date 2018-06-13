﻿# 公開時の設定

- 公開名: `FizzBuzzゲーム`
- 説明: `FizzBuzzゲームを行うスキルです。`
- 詳細な説明:

```txt
FizzBuzz（フィズバズ）ゲームを行うスキルです。
FizzBuzzゲームとは、1から順に数字を読み上げ、その数字が3で割り切れるときはFizz（フィズ）、5で割り切れるときはBuzz（バズ）、3と5の両方で割り切れるときはFizzBuzz（フィズバズ）を数字の代わりに言います。間違ったり詰まったりしたら負けです。
アレクサと交互に言い合い、間違えた時点でゲーム終了です。順番はゲームスタートのタイミングでアレクサが決めます。
アレクサは間違えないハズなので、限界まで挑戦してみてください。
```

- サンプルフレーズ:
  - `アレクサ、フィズバズゲームをスタート`
  - `アレクサ、フィズバズゲームでゲームをしよう`
  - `アレクサ、フィズバズゲームをしよう`
- カテゴリー: `Games`
- キーワード: `Fizz`, `Buzz`, `FizzBuzz`, `フィズバズ`, `フィズ`, `バズ`, `ふぃずばず`, `ふぃず`, `ばず`
- プライバシーポリシーのURL:
- 利用規約のURL:
- このスキルを使って何かを購入をしたり、実際にお金を支払うことができますか？: `いいえ`
- このAlexaスキルはユーザーの個人情報を収集しますか？: `いいえ`
- このスキルは13歳未満のお子様を対象としていますか？: `いいえ`
- このスキルで広告は表示されますか？: `いいえ`
- 輸出コンプライアンス: `Checked`

- テストの手順:

```txt
フィズバズゲームをアレクサと行うための機能が一通り実装されています。
　- フィズバズゲームは以下の流れで実行します
　　1. アレクサが最初か、ユーザーが最初になるかはランダムに決まります。アレクサが先行の場合、「一」を読み上げ、ユーザーの発話を促します。アレクサが後攻の場合は直接ユーザーの発話を促します。
　　2. ユーザーの発話に対し、正解かどうか、内容に誤りがないかを評価し、必要に応じた応答を返します。正解の場合は次のアレクサのターンの読み上げを行なった後、ユーザーの発話を待ちます。不正解の場合、メッセージを読み上げた後、スキルを終了します。
　　3. ユーザーが正しい結果を返し続ける限り、2.を繰り返します。
どの数値（またはキーワード）を言うべきかはセッションで管理しています。
その他の隠し機能などは一切ありません。
```