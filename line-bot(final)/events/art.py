from line_bot_api import *
import pymysql
from linebot.models import TextSendMessage
import pymysql
import random
import string
from events.CNN_model import homework
from linebot.models import *

def art_1(event):


    FFF = '請回傳一張圖片'
    print(FFF)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=FFF))


    @handler.add(MessageEvent, message=ImageMessage)
    def CNN(event):
        print(event.message.type)

        if event.message.type == 'image':
            print('enter pic')
            image_name = ''.join(random.choice(string.ascii_letters + string.digits)
                                 for x in range(4))
            # .ascii_letters隨機生成小寫英文字母，.digits生成數字
            image_content = line_bot_api.get_message_content(event.message.id)
            image_name = image_name.upper() + '.jpg'
            print(image_name)
            path_save = './static/' + image_name
            with open(path_save, 'wb') as fd:
                for chunk in image_content.iter_content():
                    fd.write(chunk)
            type_name = homework(path_save)

        # 連線 MySQL
        # 連線 MySQL
        connInfo = {
            'host': '54.65.74.214',
            'port': 3306,
            'user': 'root',
            'passwd': 'password',
            'db': 'demo',
            'charset': 'utf8mb4'
        }

        conn = pymysql.connect(**connInfo)
        cursor = conn.cursor()

        # 圖像辨識結果

        restType = type_name

        # 依照圖像辨識及分群結果撈資料
        sql = """ SELECT 標題, 網址 FROM food_type_content WHERE type like '%{restType}%' ORDER BY RAND() LIMIT 3 ; """.format(
            restType=restType)
        cursor.execute(sql)
        results = cursor.fetchall()

        result=[]

        result.append(TextSendMessage(results[0][1]))
        result.append(TextSendMessage(results[1][1]))
        result.append(TextSendMessage(results[2][1]))



        cursor.close()
        conn.close()


        line_bot_api.reply_message(event.reply_token, result)

