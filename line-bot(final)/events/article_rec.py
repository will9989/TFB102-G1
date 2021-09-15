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

conn = pymysql.connect(**connInfo)
cursor = conn.cursor()

# 圖像辨識結果
restType = "日式料理"

# 依照圖像辨識及分群結果撈資料
sql = """ SELECT 標題, 網址 FROM food_type_content WHERE type like '%{restType}%' ORDER BY RAND() LIMIT 3 ; """.format(restType=restType)
cursor.execute(sql)
results = cursor.fetchall()
print(results[0][1])
print(results[1][1])
print(results[2][1])

cursor.close()
conn.close()
