follow this youtube channel for the code Muhammad Yunus. he has made the face recognisation and ANPR both. so i need to learn the basics
https://github.com/Muhammad-Yunus/Face-Recognition-CNN-Keras-OpenCV/tree/master 


this is the face recognisation complete code
https://github.com/Muhammad-Yunus/Materi-Training/tree/main/C.%20Facerecognition



open the google colab and run this code for training the model
step-1) 
from google.colab import drive
drive.mount('/content/drive')

step-2)

from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="/content/yolo_dataset/data.yaml", epochs=50, imgsz=640)
