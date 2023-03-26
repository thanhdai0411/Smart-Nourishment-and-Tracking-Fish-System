# import datetime
# from datetime import date
from datetime import datetime
PATH = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/time_send_mail.txt"

time_send_mail = open(PATH , 'r').read()



datetime_object = datetime.strptime(time_send_mail.strip(),"%Y-%m-%d %H:%M:%S.%f")
if time_send_mail : 
    # print(datetime_object)
    if(datetime.now() > datetime_object) :
        print(datetime.now())
        