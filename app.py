from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('3ej9Uz4+zmPjLr843gLiVZ+feobEUXwhsABkMMBeK2doTkGSBOZ23YW/vtTCmV7ZjSGVVxovoY+eyviQLhIosgG3GoJ2xSHHHDj6VKwR1vX4o7aLrt+DYaH1q34Y+sd5VH8gRKSFC7b66ifuqokpggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('79b245a008f02582c5638699d59481a3')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()