from line_bot_api import *

def contentbased_1(event):

    import numpy as np
    import pandas as pd
    from collections import defaultdict
    from numpy import seterr
    import pymysql

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
