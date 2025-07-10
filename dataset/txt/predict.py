from ultralytics import YOLO

if __name__ == '__main__':
    # Load a pretrained YOLOv8n model
    model = YOLO("/home/newPSSD/reid/ultralytics-main/dataset/txt/runs/detect/yolov83/weights/best.pt")
# load a pretrained model (recommended for training)

# Run inference on 'bus.jpg' with arguments
    results = model.predict("/home/newPSSD/reid/ultralytics-main/dataset/images/val/",conf=0.05, device=0, save=True)
