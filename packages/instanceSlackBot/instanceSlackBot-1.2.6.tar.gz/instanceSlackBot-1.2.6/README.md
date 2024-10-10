# InstanceSlackBot

このファイルは、SlackSDKにおける基本操作をより使いやすいようにインスタンスにまとめて管理できるようにまとめたものになっています。
初心者の方でも間違いを少なく、チャンネルの作成からユーザーの招待、投稿の送信などを行うことができます。
個別の使用方法を教授することはありません。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は[LICENSE](./LICENSE)ファイルを参照してください。

## 使用方法
```
pip install instanceSlackBot
```

Botトークンを事前に入手する必要があり、適切な権限が付与されていることが必要となります
```
from instanceSlackBot import SlackBotSet

instance = SlackBotSet(api_token="hogehoge")
```

## 使用しているライブラリ

このプロジェクトでは以下のライブラリを使用しています：

- [slack-sdk](https://github.com/slackapi/python-slack-sdk) - MIT License
