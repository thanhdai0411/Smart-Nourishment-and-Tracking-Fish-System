import os


exist_folder = os.path.isdir('D:\\Studyspace\\DoAn\\Aquarium\\train_complete\\train')
path = ""
if(exist_folder) :
    for model in os.listdir("D:\\Studyspace\\DoAn\\Aquarium\\train_complete\\train\\weights"):
        if(model == "best.pt") :
            path = "best.pt"
else :
    path = "yolov5s.pt"

print(path)


