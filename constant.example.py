
SUCCESS_STATUS = {"success": 1,
                  "message": "Success !!"}

ERROR_STATUS = {"success": 0,
                "message": "Error !!"}

FOLDER_SAVE_LABELS = ''
FOLDER_SAVE_IMAGES = ''
PATCH_TO_COCO12YAML = ''

BROKER_URL = ''
BROKER_PORT = ''
BROKER_USERNAME = ''
BROKER_PASSWORD = ''


def success_status(message):
    return {"success": 1, "message": message}


def fail_status(message):
    return {"success": 0, "message": message}


MONGODB_URL = "mongodb+srv://username:pass@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"
