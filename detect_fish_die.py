import torch
import cv2
from PIL import Image
import io
import numpy as np
from constant import PATH_MODEL_FISH_DIE
from multiprocessing import Process, Value



def detect_fish_die(loop_on) : 
        
    # Model
    model = torch.hub.load('.', 'custom', path=PATH_MODEL_FISH_DIE, source='local')

    # model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom
    if loop_on.value : 
                
        camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        print("Detect fish die run")
    if not loop_on.value :
        print("Detect fish die stop")
        camera.release()
        cv2.destroyAllWindows()



    try :
        while True:

            if loop_on.value == True :
                print("run")
                success, frame = camera.read()
                if success:
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                    frame = buffer.tobytes()

                    # # =====================================

                    img = Image.open(io.BytesIO(frame))
                    # results = model(img, size=640)
                    results = model(img)
                    # # results.print()
                    
                    count_detect = results.pandas().xyxy[0]['name']
                    list_count_detect = list(count_detect) 
                    
                    if(len(list_count_detect) > 0) :
                        print('Die count: ' + str(len(list_count_detect)))
                
                    img = np.squeeze(results.render())  # RGB
                    img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    # frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()

                    cv2.imshow("frame", img_BGR)
                    if cv2.waitKey(1) == ord('q'):
                        break

                    
                    # ===================================
                else:
                    pass
    except Exception :
        print("Thoat Crond")
        handle_exception()
    

def handle_exception():
    print("handle_exception")
    recording_on = Value('b', True)
    detect_fish_die(recording_on)

# recording_on = Value('b', True)
# detect_fish_die(recording_on)