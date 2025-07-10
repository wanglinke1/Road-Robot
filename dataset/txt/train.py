import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from ultralytics import YOLO



data_config = "/home/newPSSD/reid/ultralytics-main/dataset/txt/dataset.yaml"


model = YOLO("/home/newPSSD/reid/ultralytics-main/dataset1/yolo11n.pt")  


model.train(data=data_config, epochs=1000, imgsz=640, batch=64, name='yolov8')