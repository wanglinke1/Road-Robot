import cv2
from ultralytics import YOLO

# 加载 YOLO 模型
model = YOLO("D:/pycharm/codepython/ultralytics-main/dataset/txt/runs/detect/train2/weights/best.pt")  # 替换为你的权重文件路径

# 打开摄像头
cap = cv2.VideoCapture(1)  # 参数为 0 表示使用默认摄像头

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 读取视频帧
    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        break

    # 使用 YOLO 模型进行检测
    results = model(frame)

    # 遍历检测结果并绘制
    for result in results[0].boxes:
        # 获取检测框的坐标、类别和置信度
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # 检测框坐标
        conf = result.conf[0]  # 置信度
        cls = int(result.cls[0])  # 类别索引
        label = f"{model.names[cls]} {conf:.2f}"  # 类别名称和置信度
        if conf > 0.2:
        # 绘制检测框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 绘制类别和置信度
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示结果
    cv2.imshow("YOLO Detection", frame)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()