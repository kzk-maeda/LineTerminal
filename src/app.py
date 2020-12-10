import os
import json
import logging
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
  InvalidSignatureError
)

from linebot.models import (
  MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage
)

from views.serverSelecter import ServerSelecter

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


# Read Keys
ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN', 'DUMMY')
SECRET = os.getenv('LINE_SECRET', 'DUMMY')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route('/health')
def health_check():
    app.logger.info('Health Check : OK')
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request_body : " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    app.logger.info("Handle Message")

    server_list = [
        {'name': 'ServerA', 'local_ip': '10.0.0.1'},
        {'name': 'ServerB', 'local_ip': '10.0.0.2'},
        {'name': 'ServerC', 'local_ip': '10.0.0.3'}
    ]

    serverSelecter = ServerSelecter()
    contents = serverSelecter.createCarousel(server_list)
    message = FlexSendMessage(alt_text="hello", contents=contents)
    # message = TextSendMessage(text=event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        message
    )


if __name__ == "__main__":
    app.run()