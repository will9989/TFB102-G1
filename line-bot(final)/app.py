from flask import Flask, request, abort
from line_bot_api import *
from events.appointment import appointment_step1
from events.res import res_1
from events.art import art_1
from linebot.models import *
from events.gensim import gen

app = Flask(__name__)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    print(message_text)
    if message_text == 'test1':
        appointment_step1(event)
    elif message_text == 'test2':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入一句話'))

        @handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            gen(event)



        #return HttpResponse()
@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    if ts == '餐廳':
        res_1(event)
    if ts == '文章':
        art_1(event)





if __name__ == "__main__":
	app.run()