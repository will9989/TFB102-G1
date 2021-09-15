from line_bot_api import *
from linebot.models import TextSendMessage
from gensim import corpora, models, similarities
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity, Similarity
from gensim.models import LsiModel
import jieba
import pymysql

def gen(event):
    print('v2')


    # load file
    dictionary = corpora.Dictionary.load('dictionary.dict')

    corpus_lsi = corpora.MmCorpus('corpus_lsi.mm')

    index = Similarity.load("index.index")

    model = LsiModel.load('lsi.model')
    sec = event.message.text

    new_doc = '{}'.format(sec)
    new_seg_result = jieba.lcut(new_doc)
    new_doc_bow = dictionary.doc2bow(new_seg_result)
    new_doc_lsi = model[new_doc_bow]
    sims = index[new_doc_lsi]
    sims = sorted(enumerate(sims), key=lambda i: -i[1])
    print(sims)
    print('sim{}'.format(len(sims)))

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
    list1 = []
    for i in range(0, 3):
        index0 = int(sims[i][0])
        sql = """ SELECT  sims_id, 網址 FROM LSI_df WHERE sims_id={index} ; """.format(index=index0)
        cursor.execute(sql)
        results = cursor.fetchall()
        results = list(results)

        results = results[0][1]
        #     results[0][1]

        list1.append(results)
    result=[]
    result.append(TextSendMessage(list1[0]))
    result.append(TextSendMessage(list1[1]))
    result.append(TextSendMessage(list1[2]))
    cursor.close()
    conn.close()

    line_bot_api.reply_message(event.reply_token, result)