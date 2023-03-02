
SUCCESS_STATUS = {"success": 1,
                  "message": "Success !!"}

ERROR_STATUS = {"success": 0,
                "message": "Error !!"}

FOLDER_SAVE_LABELS = 'D:\\Studyspace\\DoAn\\Aquarium\\coco128\\images\\train2017'
FOLDER_SAVE_IMAGES = 'D:\\Studyspace\\DoAn\\Aquarium\\coco128\\labels\\train2017'

PATCH_TO_COCO12YAML = "D:\\Studyspace\\DoAn\\Aquarium\\data\\coco128.yaml"
PATH_TO_WEIGHT_INIT = "D:\\Studyspace\\DoAn\\Aquarium\\yolov5n.pt"
PATCH_COUNT_FISH = 'D:\\Studyspace\\DoAn\\Aquarium\\count_fish.py'

PATH_TRAIN_MODEL = "D:\\Studyspace\\DoAn\\Aquarium\\train.py"

CLOUDINARY_NAME = 'img-aquarium'
CLOUDINARY_API_KEY = '297934749829863'
CLOUDINARY_API_SECRET = 'gtbtgeyPmx219CYa67cEqnHZ9xU'

PATCH_FOOD_SETTING = 'D:\\Studyspace\\DoAn\\Aquarium\\my_data\\food_setting.json'

BROKER_URL = 'e9b685676e514fb18a77577bc6449f0c.s1.eu.hivemq.cloud'
BROKER_PORT = 8883
BROKER_USERNAME = 'thanhdai0411'
BROKER_PASSWORD = 'thanhdai0411'


def success_status(message):
    return {"success": 1, "message": message}


def res_success(message, data):
    return {"success": 1, "message": message, "data": data}


def fail_status(message):
    return {"success": 0, "message": message}


MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"
