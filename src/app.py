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
from views.terminal import Terminal

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

    # TODO: branch by sent command
    # whether connect to server or execute remote command

    server_list = [
        {'name': 'ServerA', 'os_name': 'centos7'},
        {'name': 'ServerB', 'os_name': 'ubuntu1804'},
        {'name': 'ServerC', 'os_name': 'ubuntu1604'}
    ]

    serverSelecter = ServerSelecter()
    contents = serverSelecter.createCarousel(server_list)
    message = FlexSendMessage(alt_text="hello", contents=contents)
    # message = TextSendMessage(text=event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        message
    )


@handler.add(PostbackEvent)
def handle_postback(event):
    app.logger.info('Postback Event')

    # TODO: Connect to remote host

    terminal = Terminal()
    response_content = terminal.createTerminalResponse('ServerA', '/usr/local')

    send_line_api(event, response_content)


def send_line_api(event, contents, alt_text="text"):
    message = FlexSendMessage(alt_text=alt_text, contents=contents)

    line_bot_api.reply_message(
        event.reply_token,
        message
    )

    return 'OK'


if __name__ == "__main__":
    app.run()