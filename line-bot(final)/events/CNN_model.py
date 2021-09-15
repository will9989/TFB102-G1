import numpy as np
import os
from sklearn.metrics import confusion_matrix
import seaborn as sn; sn.set(font_scale=1.4)
from sklearn.utils import shuffle           
import matplotlib.pyplot as plt             
import cv2                                 
import tensorflow as tf                
from tqdm import tqdm
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.models import load_model

# from keras.models import load_model
# model = load_model('food_model')
def homework(path):

    model = load_model('food_model')
    remote_image = path
    img = cv2.imread(remote_image,1)#cv2.IMREAD_GRAYSCALE
    img = cv2.cvtColor(img,0)
    # plt.imshow(cv2.cvtColor(img,0))#cv2.IMREAD_GRAYSCALE
    img = cv2.resize(img, (64, 64))
    img = img/255.0
    img = np.asarray(img).reshape(-1,64, 64,4)

    result = np.argmax(model.predict(img)) #model.predict(img)抓這行出來看分數
    print(result)
    type_ = {'0': '美式料理', '1': '亞洲料理', '2': '酒吧','3':'烤肉','4':'咖啡廳','5':'中式料理','6':'歐式料理','7':'法式料理'\
             ,'8':'燒肉','9':'日式料理','10':'韓式料理','11':'義式料理','12':'多國','13':'海鮮','14':'壽司','15':'台灣小吃'\
            ,'16':'泰式料理','17':'素食','18':'提供素食料理py'}
    type_name=type_[str(result)]
    # print(type_name)

    return type_name

# if __name__ == '__main__':
#     remote_image_url = homework('./A3.jpg')   