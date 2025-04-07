from remedies.models import Remedy 
import json
import requests
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient


# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Niramay"]

# Collections for Remedies, Plants, and Recipes
collection_remedies = db["remedies"]
collection_plants = db["plants"]
collection_recipes = db["recipes"]

# --- STATIC PAGES ---
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')



def symptoms(request):
    return render(request, 'symptoms.html')

def find_options(request):
    return render(request, 'find_options.html')

def chatbot(request):
    return render(request, 'chatbot.html')

# --- REMEDIES HANDLING ---
from django.shortcuts import render
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Niramay"]
collection_remedies = db["remedies"]
def remedies(request):
    """Fetch remedies from MongoDB based on user symptom and severity."""
    symptom = request.GET.get("symptom", "").strip().lower()  # Normalize input
    selected_severity = request.GET.get("severity", "Mild").capitalize()  # Default to 'Mild'

    if not symptom:
        return render(request, "remedies.html", {"error": "Please enter a symptom."})

    # ✅ Fix: Case-Insensitive Query for MongoDB
    remedy_data = collection_remedies.find_one({"symptom": {"$regex": f"^{symptom}$", "$options": "i"}}, {"_id": 0})

    if not remedy_data:
        return render(request, "remedies.html", {"symptom": symptom, "error": "No remedies found."})

    # Process ayurvedic remedies for selected severity
    ayurvedic_remedies = [
        {
            "name": remedy["name"],
            "selected_dosage": remedy["dosage"].get(selected_severity, "Dosage not available")
        }
        for remedy in remedy_data.get("ayurvedic_remedies", [])
    ]

    return render(request, "remedies.html", {
        "symptom": symptom.capitalize(),
        "selected_severity": selected_severity,
        "ayurvedic_remedies": ayurvedic_remedies,
        "home_remedies": remedy_data.get("home_remedies", []),
        "diet_recommendations": remedy_data.get("diet_recommendations", [])
    })
def filter_remedies(request):
    return JsonResponse({"message": "Filter remedies endpoint working"})

# --- PLANTS HANDLING ---
def plants(request):
    """Search for plant information."""
    if request.method == "POST":
        plant_name = request.POST.get("plant_name", "").strip().lower()
        if plant_name:
            return redirect(f"/plants_features/{plant_name}/")
    return render(request, "plants.html")

def plants_features(request, plant_name):
    """Fetch plant details from MongoDB."""
    plant_info = collection_plants.find_one(
        {"$or": [
            {"name": {"$regex": f"^{plant_name}$", "$options": "i"}},
            {"scientific_name": {"$regex": f"^{plant_name}$", "$options": "i"}}
        ]},
        {"_id": 0}  # Exclude MongoDB ID
    )

    if plant_info and "image_url" not in plant_info:
        plant_info["image_url"] = "/static/images/default-plant.jpg"

    return render(request, "plants_features.html", {"plant_info": plant_info})

# --- RECIPES HANDLING ---
def recipes_list(request):
    """Fetch all recipes from MongoDB."""
    try:
        recipes = list(collection_recipes.find({}, {"_id": 0}))  # Fetch recipes
        return render(request, 'recipes.html', {'recipes': recipes})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

# --- DATABASE TEST FUNCTION ---
def test_connection():
    """Test if MongoDB is connected."""
    try:
        count = collection_recipes.count_documents({})
        print(f"Connected! Total Recipes: {count}")
    except Exception as e:
        print("Connection Error:", e)

import os
from django.shortcuts import render
from django.conf import settings
from ml_models.predict_plant_model import predict_plant_from_image  # Corrected import

def predict_plant_view(request):
    plant_name = None

    if request.method == 'POST' and request.FILES.get('leaf_image'):
        uploaded_file = request.FILES['leaf_image']
        image_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        # Save image to media folder
        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Predict the plant name
        plant_name = predict_plant_from_image(image_path)

    return render(request, 'predict_plant.html', {'plant_name': plant_name})

def plants_features_redirect(request):
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name').strip().lower()
        return redirect('plants_features', plant_name=plant_name)
