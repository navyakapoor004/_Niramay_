import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

MODEL_DIR = "C:/DTI_NAVYA/Niramay/ml_models"
DATASET_PATH = "C:/DTI_NAVYA/Niramay/media/Segmented Medicinal Leaf Images"

os.makedirs(MODEL_DIR, exist_ok=True)

def extract_features(image):
    image = cv2.resize(image, (128, 128))

    # Color Histogram
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    # Hu Moments
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(gray)
    huMoments = cv2.HuMoments(moments).flatten()

    return np.hstack([hist, huMoments])

def load_dataset():
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset path '{DATASET_PATH}' not found!")
        return None, None

    X, y = [], []
    for label in os.listdir(DATASET_PATH):
        label_path = os.path.join(DATASET_PATH, label)
        if os.path.isdir(label_path):
            for file in os.listdir(label_path):
                file_path = os.path.join(label_path, file)
                img = cv2.imread(file_path)
                if img is not None:
                    features = extract_features(img)
                    X.append(features)
                    y.append(label)

    if len(X) == 0:
        print("❌ No valid images found!")
        return None, None

    return np.array(X), np.array(y)

def train_model():
    X, y = load_dataset()
    if X is None or y is None:
        return

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model Trained! Accuracy: {acc:.4f}")

    joblib.dump(model, os.path.join(MODEL_DIR, "plant_model.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))
    print(f"✅ Model saved at '{MODEL_DIR}/plant_model.pkl'")

if __name__ == "__main__":
    train_model()
