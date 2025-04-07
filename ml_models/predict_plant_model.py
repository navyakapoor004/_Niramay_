import os
import joblib
import cv2
from .plant_detection import extract_features  # Important!

MODEL_PATH = os.path.join(os.path.dirname(__file__), "plant_model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

def predict_plant_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None

    features = extract_features(img).reshape(1, -1)
    prediction = model.predict(features)
    plant_name = label_encoder.inverse_transform(prediction)[0]
    return plant_name
