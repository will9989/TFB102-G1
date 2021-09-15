from line_bot_api import *
from linebot.models import *
from collections import defaultdict
from numpy import seterr
import pymysql
import pickle
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import random
import string 
from events.CNN_model import homework


def res_1(event):
    questionnaire = None
    userid = event.source.user_id
    db = pymysql.connect(host="54.65.74.214",
                         user="root",
                         password="password",
                         db="demo",
                         port=3306,
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute('''select count(*) from user_id_history where user_id=('%s')'''%(userid))
    data = cursor.fetchone()
    if data['count(*)'] == 0:
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(

                        title='食物偏好',
                        text='Please select service',
                        actions=[
                            PostbackAction(
                                label='高',
                                display_text='高',
                                data='A&5'

                            ),
                            PostbackAction(
                                label='中',
                                display_text='中',
                                data='A&3'
                            ), PostbackAction(
                                label='低',
                                display_text='低',
                                data='A&1'

                            )

                        ]
                    )
                ]
            )
        )


        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=[
                carousel_template_message]
        )

        @handler.add(PostbackEvent)
        def handle_postback(event):

            if event.postback.data[0:1] == "A":
                food_= event.postback.data[2:]
                carousel_template_message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(

                                title='服務偏好',
                                text='Please select service',
                                actions=[
                                    PostbackAction(
                                        label='高',
                                        display_text='高',
                                        data='B&5'

                                    ),
                                    PostbackAction(
                                        label='中',
                                        display_text='中',
                                        data='B&3'
                                    ), PostbackAction(
                                        label='低',
                                        display_text='低',
                                        data='B&1'

                                    )

                                ]
                            )
                        ]
                    )
                )

                line_bot_api.reply_message(
                    reply_token=event.reply_token,
                    messages=[
                        carousel_template_message]
                )

                @handler.add(PostbackEvent)
                def handle_postback(event):

                    if event.postback.data[0:1] == "B":
                        ser_ = event.postback.data[2:]
                        carousel_template_message = TemplateSendMessage(
                            alt_text='Carousel template',
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(

                                        title='實惠偏好',
                                        text='Please select service',
                                        actions=[
                                            PostbackAction(
                                                label='高',
                                                display_text='高',
                                                data='C&5'

                                            ),
                                            PostbackAction(
                                                label='中',
                                                display_text='中',
                                                data='C&3'
                                            ), PostbackAction(
                                                label='低',
                                                display_text='低',
                                                data='C&1'

                                            )

                                        ]
                                    )
                                ]
                            )
                        )

                        line_bot_api.reply_message(
                            reply_token=event.reply_token,
                            messages=[
                                carousel_template_message]
                        )

                        @handler.add(PostbackEvent)
                        def handle_postback(event):

                            if event.postback.data[0:1] == "C":
                                cp_ = event.postback.data[2:]
                                carousel_template_message = TemplateSendMessage(
                                    alt_text='Carousel template',
                                    template=CarouselTemplate(
                                        columns=[
                                            CarouselColumn(

                                                title='環境偏好',
                                                text='Please select service',
                                                actions=[
                                                    PostbackAction(
                                                        label='高',
                                                        display_text='高',
                                                        data='D&5'

                                                    ),
                                                    PostbackAction(
                                                        label='中',
                                                        display_text='中',
                                                        data='D&3'
                                                    ), PostbackAction(
                                                        label='低',
                                                        display_text='低',
                                                        data='D&1'

                                                    )

                                                ]
                                            )
                                        ]
                                    )
                                )
                                line_bot_api.reply_message(
                                    reply_token=event.reply_token,
                                    messages=[
                                        carousel_template_message]
                                )         
                                @handler.add(PostbackEvent)
                                def handle_postback(event):
                                    print('enter')

                                    if event.postback.data[0:1] == "D":
                                        print('D')

                                        env_ = event.postback.data[2:]
                                        questionnaire = [int(food_), int(ser_), int(cp_), int(env_)]
                                        print(questionnaire)
                                        FFF='請回傳一張圖片'
                                        print(FFF)
                                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=FFF))
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

                                        # 載入 K-means 模型
                                        with open("./kmeansmodel.pkl", "rb") as f:
                                            model = pickle.load(f)

                                        # 圖像辨識結果
                                        restType = type_name

                                        # user line 編號
                                        user_id = event.source.user_id

                                        # 問卷答案輸入及分群預測
                                        # questionnaire = [int(input()), int(input()), int(input()), int(input())]
                                        predicted_cluster = model.predict([questionnaire]).tolist()[0]

                                        # 依照圖像辨識及分群結果撈資料
                                        sql = """ select id, 餐廳名稱, 餐廳網站 from kmeans_with_sum_score where clustering = {predicted_cluster} and 餐廳類型 like '%{restType}%' order by 評論分數 desc limit 3; """.format(
                                            predicted_cluster=predicted_cluster, restType=restType)
                                        cursor.execute(sql)
                                        results = cursor.fetchall()

                                        # 將查詢結果存入 MySQL
                                        sql_insert = """ insert into user_id_history values (%s, %s, %s, %s, %s); """
                                        rating = sum(i for i in questionnaire) / 4
                                        values = [(user_id,) + (rating,) + t for t in results]
                                        cursor.executemany(sql_insert, values)
                                        conn.commit()
                                        cursor.close()
                                        conn.close()

                                        # 印出結果
                                        print('result by kmeans')
                                        reply_arr = []
                                        reply_arr.append(TextSendMessage(results[0][2]))
                                        reply_arr.append(TextSendMessage(results[1][2]))
                                        reply_arr.append(TextSendMessage(results[2][2]))
                                        line_bot_api.reply_message(event.reply_token, reply_arr)

                                




    else:

        # 連線 MySQL
        connInfo={
            'host': '54.65.74.214',
            'port': 3306,
            'user': 'root',
            'passwd': 'password',
            'db': 'demo',
            'charset': 'utf8mb4'
        }

        conn=pymysql.connect(**connInfo)
        cursor=conn.cursor()

        # user line 編號
        user_id = event.source.user_id

        # 依照 user line 編號撈資料
        sql_query = """ select 餐廳名稱, rating from user_id_history where user_id = ('%s') """%(user_id)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        Lawrence_ratings = []
        for i in results:
            Lawrence_dict = {}
            Lawrence_dict['name'] = i[0]
            Lawrence_dict['rating'] = i[1]
            Lawrence_ratings.append(Lawrence_dict)

        # 將 MySQL table 轉 pandas
        sql_read = """ select * from trip_tag_final; """
        res = pd.read_sql(sql_read, conn)

        # 推薦餐廳運算
        Lawrence_ratings = pd.DataFrame(Lawrence_ratings)
        Lawrence_ratings = Lawrence_ratings.drop_duplicates()
        Lawrence_Id = res[res['name'].isin(Lawrence_ratings['name'])]
        Lawrence_ratings=pd.merge(Lawrence_Id, Lawrence_ratings)
        Lawrence_ratings=Lawrence_ratings[['_id','name','rating']]
        r1=res.copy()
        r1=r1[['_id','finalsc','food','serv','cp','atmosphere','亞洲料理','中式料理','台灣小吃','台菜','日式料理','咖啡廳','義式料理','美式料理','海鮮','酒吧','多國料理','牛排','提供素食選擇','燒烤','提供純素選擇','壽司','泰式料理','法式料理','烤肉','歐式料理','韓式料理']]
        Lawrence_Id = res[res['name'].isin(Lawrence_ratings['name'])]
        Lawrence_ratings=pd.merge(Lawrence_Id, Lawrence_ratings)
        Lawrence_ratings=Lawrence_ratings[['_id','name','rating']]
        Lawrence_genres_df = r1[r1._id.isin(Lawrence_ratings._id)]
        ll1=Lawrence_genres_df.copy(deep=True)
        ll1.reset_index(drop=True, inplace=True)

        ll1.drop(['finalsc','finalsc','food','serv','cp','atmosphere'], axis=1, inplace=True)
        ll1.drop(['_id'], axis=1, inplace=True)
        res__profile=ll1.T.dot(Lawrence_ratings.rating)
        r2=res.copy()
        Lawrence_genres_df = r2.set_index(res._id)
        Lawrence_genres_df.drop(['_id','id','name','url','rank','add','phone','phone','price','type','finalsc','food','serv','cp','atmosphere'], axis=1, inplace=True)
        recommendation_table_df=(Lawrence_genres_df.dot(res__profile)) / res__profile.sum()
        recommendation_table_df.sort_values(ascending=False, inplace=True)
        copy = res.copy(deep=True)
        copy = copy.set_index('_id', drop=True)
        top_3_index = recommendation_table_df.index[:3].tolist()
        recommended_res = copy.loc[top_3_index, :]
        recomm = recommended_res[['id','name','url']]
        temp = []
        for i in recomm.values.tolist():
            i = tuple(i)
            temp.append(i)
        results = tuple(temp)

        # 將查詢結果存入 MySQL
        sql_insert = """ insert into user_id_history values (%s, %s, %s, %s, %s); """
        rating = Lawrence_dict['rating']
        values = [(user_id,) + (rating,) + t for t in results]
        cursor.executemany(sql_insert, values)
        conn.commit()
        cursor.close()
        conn.close()

        # 印出結果
        print('result by content-based')
        reply_arr=[]
        reply_arr.append(TextSendMessage(results[0][2]))
        reply_arr.append(TextSendMessage(results[1][2]))
        reply_arr.append(TextSendMessage(results[2][2]))
        line_bot_api.reply_message(event.reply_token, reply_arr)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='有會員'))

    cursor.close()