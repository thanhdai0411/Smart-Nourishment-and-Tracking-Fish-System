
SUCCESS_STATUS = {"success": 1,
                  "message": "Success !!"}

ERROR_STATUS = {"success": 0,
                "message": "Error !!"}

BASE_PATH = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart"

EPOCH_TRAIN = 100

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


PATH_MODEL_FISH_NAME = BASE_PATH + "/best_s_29.pt"

FOLDER_TRAIN_COMPLETE = BASE_PATH+ '/train_complete'

CLOUDINARY_NAME = 'img-aquarium'
CLOUDINARY_API_KEY = '297934749829863'
CLOUDINARY_API_SECRET = 'gtbtgeyPmx219CYa67cEqnHZ9xU'

PATCH_FOOD_SETTING = BASE_PATH + '/my_data/food_setting.json'


# BROKER_URL = '192.168.1.28'
# BROKER_PORT = 1883
# BROKER_USERNAME = 'aquarium'
# BROKER_PASSWORD = 'aquarium123@'


BROKER_URL = "192.168.1.28"
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
