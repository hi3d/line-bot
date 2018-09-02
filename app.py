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

line_bot_api = LineBotApi('0vi6mNh6bcrAui+8OHa0MBKIOyR8bFIbrTyzwi0V4OVj78I1eFoJgsgYeBnvOGkLjSGVVxovoY+eyviQLhIosgG3GoJ2xSHHHDj6VKwR1vWabEl2KE0HoyXatGP90Cnhy0HKrUTw7DylhSH7IJduYAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1363c7906451bdcfb872329778e0ff87')


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
    msg = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你好"))


if __name__ == "__main__":
    app.run()