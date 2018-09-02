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

line_bot_api = LineBotApi('6bUCVTotlYiDP/HmSyt5C5aYD6uQ9uUNwO8rFAfJgel3Fwcbw6BiwNPqUwcciJc/jSGVVxovoY+eyviQLhIosgG3GoJ2xSHHHDj6VKwR1vV8glKtwWaZyi7XK27CwUiCPFNTAGJ4DKktNMWG3CZGCgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('440bf1298cc9caf184b2a48f8c0f2d6f')


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