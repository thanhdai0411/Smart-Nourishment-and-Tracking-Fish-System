BASE_PATH = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart"

AI_FILE_SAVE_MODEL = BASE_PATH + '/ai_feeder/ai_feeder.h5'
MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"

import dns.resolver as dnsr
dnsr.default_resolver =  dnsr.Resolver(configure=False)
dnsr.default_resolver.nameservers = ["8.8.8.8"]


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

import pymongo
myclient = pymongo.MongoClient(MONGODB_URL)
mydb = myclient["test"]
colection_amount_fish = mydb["amount_fish"]

import pandas as pd
import numpy as np

# get all data from db with collection  "amount_fish"
data_fish = colection_amount_fish.find()


# dupticate data
amount_repeat = 10
data_fish = np.repeat(list(data_fish), amount_repeat)


print(len(list(data_fish)))

# for x in data_fish:
#     print(x)
    

# handle data
data_fish = colection_amount_fish.find()

data_final  = []

for x in data_fish:
    
    list_data_fish_count = x["fish_count"]  
    amount_food = x["amount_eat"]


    list_amount_fish = []

    for data_fc in list_data_fish_count :
        list_amount_fish.append(data_fc["amount"])
    data_final.append({
        "amount_food" : amount_food, 
        "list_amount_fish" : list_amount_fish

    })

# tim max_length de add cho tat ca cac lish_amount_fish bang nhau de tao dataframe
max_length = max(len(d["list_amount_fish"]) for d in data_final)

# loop data de add cho bang nhau het
for i, d in enumerate(data_final):
    padded_array = d["list_amount_fish"] + [0] * (max_length - len(d["list_amount_fish"]))

    d["list_amount_fish"] = padded_array


# print(data_final)



# Tạo dữ liệu huấn luyện và kiểm tra
X = []
y = []

for sample in data_final:
    X.append([x for x in sample['list_amount_fish']])
    y.append(float(sample['amount_food']))
 
#======================================================
'''

# train_size = int(len(X) * 0.7)
# X_train, X_test = X[:train_size], X[train_size:]
# y_train, y_test = y[:train_size], y[train_size:]


# X_train = np.array(X_train).reshape(len(X), -1, 1)
# X_test = np.array(X_test).reshape(len(X_test), -1, 1)

# y_train = np.array(y_train).reshape(-1, 1)
# y_test = np.array(y_test).reshape(-1, 1)
'''
#======================================================


X_train = np.array(X).reshape(len(X), -1, 1)
y_train = np.array(y).reshape(-1, 1)

model = Sequential()

# model.add(LSTM(64, input_shape=(None, 1)))
# model.add(Dense(1, activation='linear'))

model.add(LSTM(128, return_sequences=True, input_shape=(None, 1)))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear'))


model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=100, batch_size=32)

'''
# Đánh giá mô hình trên dữ liệu kiểm tra
loss = model.evaluate(X_test, y_test)
print("Loss:", loss)
'''

# save model
model.save(AI_FILE_SAVE_MODEL)

# model_save = tf.keras.models.load_model(AI_FILE_SAVE_MODEL)


# X_new = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 2, 3, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# X_new = [[4, 2, 3, 2, 2, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 1, 2, 1, 0, 0, 0, 2, 0, 0, 1]]
# X_new = tf.reshape(X_new, (len(X_new), len(X_new[0]), 1))

# predictions = model_save.predict(X_new)

# print("Predictions Amount Food:", predictions)
# print("Predictions Amount Food:", round(predictions[0][0], 4))

# predictions = model.predict(X_new)
# print("Predictions Amount Food:", predictions)