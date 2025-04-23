from pymongo import MongoClient
import json
import os

# ✅ MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["niramay_db"]
collection_remedies = db["remedies"]

# ✅ File Path for Remedies Data
file_path_remedies = "C:/DTI_NAVYA/data/data.json"

# ✅ Step 1: Load Remedies Data from `data.json`
if os.path.exists(file_path_remedies):
    with open(file_path_remedies, "r", encoding="utf-8") as file:
        remedies_data = json.load(file)

    # ✅ Insert Data Only if Collection is Empty
    if collection_remedies.count_documents({}) == 0:
        collection_remedies.insert_many(remedies_data)
        print("✅ Remedies Data Inserted Successfully!")
    else:
        print("✅ Remedies Already Exists in Database!")

else:
    print("❌ Error: data.json file not found!")

# ✅ Step 2: Take Allergy Input from User
user_allergy = input("\n⚠ Enter the ingredient you are allergic to: ").strip().lower()

# ✅ Step 3: Fetch and Filter Remedies from MongoDB
all_remedies = list(collection_remedies.find())

filtered_remedies = []
for remedy in all_remedies:
    ayurvedic = remedy.get("ayurvedic_remedies", [])
    home = remedy.get("home_remedies", [])
    diet = remedy.get("diet_recommendations", [])

    # ✅ Remove Remedies Containing Allergic Ingredient
    ayurvedic = [r for r in ayurvedic if user_allergy not in r.lower()]
    home = [r for r in home if user_allergy not in r.lower()]
    diet = [r for r in diet if user_allergy not in r.lower()]

    # ✅ If at least one valid recommendation remains, add to filtered list
    if ayurvedic or home or diet:
        filtered_remedies.append({
            "symptom": remedy.get("symptom", "Unknown"),
            "ayurvedic_remedies": ayurvedic,
            "home_remedies": home,
            "diet_recommendations": diet
        })

# ✅ Step 4: Output Final Remedies After Allergy Check
print("\n✅ Final Remedies After Allergy Check:")
if filtered_remedies:
    for remedy in filtered_remedies:
        print(f"- Symptom: {remedy.get('symptom', 'Unknown')}")
        
        ayurvedic = ", ".join(remedy.get("ayurvedic_remedies", []) or ["No Ayurvedic Remedies"])
        home = ", ".join(remedy.get("home_remedies", []) or ["No Home Remedies"])
        diet = ", ".join(remedy.get("diet_recommendations", []) or ["No Diet Recommendations"])
        
        print(f"  Ayurvedic Remedies: {ayurvedic}")
        print(f"  Home Remedies: {home}")
        print(f"  Diet Recommendations: {diet}\n")
else:
    print("❌ No suitable remedies found after allergy check.")
