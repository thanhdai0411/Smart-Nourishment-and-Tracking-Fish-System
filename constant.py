
SUCCESS_STATUS = {"success": 1,
                  "message": "Success !!"}

ERROR_STATUS = {"success": 0,
                "message": "Error !!"}

BASE_PATH = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart"

EPOCH_TRAIN = 50

FOLDER_SAVE_LABELS = BASE_PATH + '/coco128/labels/train2017'
FOLDER_SAVE_IMAGES = BASE_PATH + '/coco128/images/train2017'

PATCH_TO_COCO12YAML = BASE_PATH + "/data/coco128.yaml"
PATH_TO_WEIGHT_INIT_5N = BASE_PATH + "/yolov5n.pt"

PATCH_COUNT_FISH = BASE_PATH + '/count_fish.py'

PATH_TRAIN_MODEL = BASE_PATH + "/train.py"
PATH_MODEL_FISH_DIE = BASE_PATH + "/model_fish_die_new.pt"
PATH_MODEL_USER_CUSTOM_NAME = BASE_PATH + "/train_complete/train/weights/best.pt"


PATH_SAVE_STATE_LOAD_FISH_DIE = BASE_PATH + "/my_data/load_fish_die.txt"
PATH_SAVE_TIME_SEND_MAIL = BASE_PATH + "/my_data/time_send_mail.txt"
PATH_SAVE_INFO_FEEDER = BASE_PATH + "/my_data/info_feeder.json"
PATH_SAVE_DATE_UPDATE_DAILY_FOOD = BASE_PATH + "/my_data/update_daily_state_food.txt"

PATH_SAVE_STATE_LOAD_MODEL_DETECT = BASE_PATH + "/my_data/load_model_detect.txt"



# PATH_MODEL_FISH_NAME = BASE_PATH + "/best_s_19_5.pt"
# /home/doan/Desktop/DA/WebServer/Aquarium-Smart/train_complete/train/weights/best.pt
PATH_MODEL_FISH_NAME = BASE_PATH + "/train_complete/train/weights/best.pt"

FOLDER_TRAIN_COMPLETE = BASE_PATH+ '/train_complete'

CLOUDINARY_NAME = 'img-aquarium'
CLOUDINARY_API_KEY = '297934749829863'
CLOUDINARY_API_SECRET = 'gtbtgeyPmx219CYa67cEqnHZ9xU'

PATCH_FOOD_SETTING = BASE_PATH + '/my_data/food_setting.json'

#! AI

AI_FILE_SAVE_MODEL = BASE_PATH + '/ai_feeder/ai_feeder.h5'
AI_FILE_SOURCE = BASE_PATH + '/ai_feeder/ai.py'

DATA_FOR_AI = BASE_PATH + '/ai_feeder/data_for_ai.json'

RESULT_PREDIRECT_AI = BASE_PATH + '/ai_feeder/result_redirect.json'

PATH_SATE_LOAD_AI =BASE_PATH + "/my_data/load_ai.txt"

RGB_START_SYSTEM = BASE_PATH + "/rgb_start_system.py"

TIME_DURATION_LEARNING_AI = 7
DATE_LEARNING_AI = BASE_PATH + '/ai_feeder/date_learning_ai.txt'

# ! send mail notify

SEND_MAIL_NOTIFY = BASE_PATH + "/send_mail_notify.py"
SEND_MAIL_NOTIFY_TRAIN_COMPLETE = BASE_PATH + "/send_mail_train_complete.py"

# BROKER_URL = '192.168.1.28'
# BROKER_PORT = 1883
# BROKER_USERNAME = 'aquarium'
# BROKER_PASSWORD = 'aquarium123@'


BROKER_URL = "0.0.0.0"
BROKER_PORT = 1883
BROKER_USERNAME = "aquarium"
BROKER_PASSWORD = "aquarium123@"

# BROKER_URL = 'e9b685676e514fb18a77577bc6449f0c.s1.eu.hivemq.cloud'
# BROKER_PORT = 8883
# BROKER_USERNAME = 'thanhdai0411'
# BROKER_PASSWORD = 'thanhdai0411'

EMAIL_USERNAME = 'aquarium.smart.service@gmail.com'
EMAIL_PASSWORD = 'fmklaxodfduvreca'



def success_status(message):
    return {"success": 1, "message": message}


def res_success(message, data):
    return {"success": 1, "message": message, "data": data}


def fail_status(message):
    return {"success": 0, "message": message}


MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"
