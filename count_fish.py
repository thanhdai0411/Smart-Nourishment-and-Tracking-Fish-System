import cv2
import numpy as np
# import matplotlib.pyplot as plt
import time
import datetime

import paho.mqtt.client as paho
from paho import mqtt


from pymongo import MongoClient

from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD,MONGODB_URL

patch = "D:\\Studyspace\\DoAn\\Aquarium\\my_data\\12.mp4"

cap = cv2.VideoCapture(patch)


db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]


year, month, day = time.strftime(
        '%Y'), time.strftime('%m'), time.strftime('%d')

date_start =  str(day) + "-" + str(month) + "-" + str(year) 
# now_start = datetime.datetime.now().strftime("%H:%M:%S.%f")
now_start = datetime.datetime.now()



init_data = {
    "date" : date_start,
    "time_start" : now_start,
    "fish_count" : []
}

collection_name.insert_one(init_data)


if not cap.isOpened():
    print("Cannot open camera")
    exit()


DURATION = 30

EDGE_TOP = 50
EDGE_RIGHT = 500
EDGE_BOTTOM = 350
EDGE_LEFT = 100

TIME_DURATION = datetime.datetime.now() + datetime.timedelta(seconds=DURATION)
# time_duration = datetime.datetime.now()+datetime.timedelta(minutes=DURATION)

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connect MQTT Count Fish ")

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))



client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
client.connect(BROKER_URL, BROKER_PORT)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# client.subscribe("control_lamp", qos=1)
item_details = collection_name.find_one({"time_start" : now_start})
data_start_trans = str(1)+"="+str(item_details["_id"])
client.publish("feed_fish", payload=data_start_trans, qos=1)

client.loop_start()
    
while True:

    _, img = cap.read()

    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_cvtc = img_cvt.copy()
    cv2.rectangle(img_cvtc, (EDGE_LEFT, EDGE_TOP),
                  (EDGE_RIGHT, EDGE_BOTTOM), (0, 0, 255), 5)

    ROI = img_cvt[EDGE_TOP:EDGE_BOTTOM, EDGE_LEFT:EDGE_RIGHT]

    gray = cv2.cvtColor(ROI, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    ret, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(
        threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt_info = []

    fish_contour = np.zeros(threshold.shape)
    count = 0
    for cnt in contours:

        area = round(cv2.contourArea(cnt))

        if area > 50 and 0 not in cnt:

            if 0 or threshold.shape[1] - 1 not in (cnt[i][0][0] for i in range(len(cnt))):

                if 0 or threshold.shape[0] - 1 not in (cnt[i][0][1] for i in range(len(cnt))):

                    cv2.drawContours(fish_contour, [cnt], 0, 255, -1)

                    count = count + 1

    #! show frame
    # cv2.imshow("Edge", img_cvtc)
    # cv2.imshow("Thresh", fish_contour)

    year, month, day = time.strftime(
        '%Y'), time.strftime('%m'), time.strftime('%d')

    # now = datetime.datetime.now().strftime("%H:%M:%S.%f")
    now = datetime.datetime.now()

    # timing = time.strftime('%H:%M:%S:%F')


    
    date_push =  str(day) + "-" + str(month) + "-" + str(year) 
    fish_count =  {"time" : now,"amount" : count}

    data_trans =  str(now) + "=" + str(count)
    
    client.publish("count_fish", payload=data_trans, qos=1)


    collection_name.update_one({"date" : date_push,"time_start" : now_start},{"$push" : {"fish_count" :fish_count}})


    time.sleep(0.3)

    if datetime.datetime.now() > TIME_DURATION:
        data_start_trans = str(0)+"="+str(item_details["_id"])
        client.publish("feed_fish", payload=data_start_trans, qos=1)
        break
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
