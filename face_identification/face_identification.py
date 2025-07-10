"""
This module contains the `FaceIdentifier` class that can be used to identify faces in a video stream.

该模块包含`FaceIdentifier`类，可用于在视频流中识别人脸。
"""
# import libraries
import os
import cv2
import imutils
# import time
import pickle
import numpy as np
# from imutils.video import FPS
# from imutils.video import VideoStream

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))


class FaceIdentifier:
    """
    A class that can be used to identify faces in a video stream.
    
    一个可用于在视频流中识别人脸的类。
    """
    def __init__(self):
        """
        Initialize the `FaceIdentifier` object.

        初始化`FaceIdentifier`对象。
        """
        # load serialized face detector
        print("Loading Face Detector...")
        protoPath = "/face_detection_model/deploy.prototxt"
        modelPath = "/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
        self.detector = cv2.dnn.readNetFromCaffe(current_dir + protoPath, current_dir + modelPath)

        # load serialized face embedding model
        print("Loading Face Recognizer...")
        self.embedder = cv2.dnn.readNetFromTorch(current_dir + "/assets/openface_nn4.small2.v1.t7")

        # load the actual face recognition model along with the label encoder
        # recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())
        self.recognizer = pickle.loads(open(current_dir + "/output/recognizer", "rb").read())
        self.le = pickle.loads(open(current_dir + "/output/le.pickle", "rb").read())

    def use(self, frame):
        """
        Identify faces in the given `frame`.

        在给定的`frame`中识别人脸。

        Args:
            frame: The frame to identify faces from.

        Returns:
            A tuple containing the following elements:
            - The annotated frame.
            - The number of faces detected in the frame.
            - The bounding boxes of the faces detected in the frame.

            包含以下元素的元组：
            - 带标注的帧。
            - 在帧中检测到的人脸数量。
            - 在帧中检测到的人脸的边界框。
        """
        detector = self.detector
        embedder = self.embedder
        recognizer = self.recognizer
        le = self.le

        # Make a copy of the frame to draw on.
        # 复制一份帧以便绘制
        frame = frame.copy()

        # resize the frame to have a width of 600 pixels.
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()
        
        # the (x, y)-coordinates of the bounding boxes for the faces
        boxes = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > 0.5:
                # compute the (x, y)-coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                boxes.append(detections[0, 0, i, 3:7])

                # construct a blob for the face ROI, then pass the blob through our face embedding model to obtain the 128-d quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                    (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                # draw the bounding box of the face along with the associated probability
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        return frame, len(boxes), boxes
