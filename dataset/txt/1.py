from ultralytics import YOLO

model = YOLO("/home/newPSSD/reid/ultralytics-main/dataset/txt/runs/detect/yolov83/weights/best.pt")  


success = model.export(format="onnx")

if success:
    print("haha")
else:
    print("failed")