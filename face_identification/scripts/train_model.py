# USAGE
# python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

import os

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(os.path.join(current_dir, "..", "output", "embeddings.pickle"), "rb").read())

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=1.0, kernel="rbf", probability=True)
recognizer.fit(data["embeddings"], labels)

# write the actual face recognition model to disk
f = open(os.path.join(current_dir, "..", "output", "recognizer"), "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(os.path.join(current_dir, "..", "output", "le.pickle"), "wb")
f.write(pickle.dumps(le))
f.close()