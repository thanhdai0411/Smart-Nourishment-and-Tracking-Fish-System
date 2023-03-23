import datetime

PATH = "D:\\Studyspace\\DoAn\\Aquarium\\my_data\\time_send_mail.txt"

time_send_mail = open(PATH , 'r').read()
print(time_send_mail)
if time_send_mail : 
    datetime_object = datetime.datetime.fromisoformat(time_send_mail.strip())
    if(datetime.datetime.now() < datetime_object) :
        print(datetime.datetime.now())
        