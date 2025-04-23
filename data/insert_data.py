import pymongo
import json
import os

# ✅ MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["niramay_db"]

# ✅ Collections
collection_remedies = db["remedies"]
collection_plants = db["plants"]
collection_recipes = db["recipes"]

# ✅ Fixing File Paths
DATA_DIR = "C:/DTI_NAVYA/data"  # Yeh directory ensure kar le ki sahi hai
file_path_remedies = os.path.join(DATA_DIR, "data.json")
file_path_plants = os.path.join(DATA_DIR, "plants.json")
file_path_recipes = os.path.join(DATA_DIR, "recipes.json")

# ✅ Function to Insert Data
def insert_data(file_path, collection, unique_field):
    """Generic function to insert data into MongoDB while avoiding duplicates."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):  # Ensure data is a list
                count = 0
                for entry in data:
                    if collection.find_one({unique_field: entry[unique_field]}) is None:
                        collection.insert_one(entry)
                        count += 1
                print(f"✅ {count} new records inserted in {collection.name}!")
            else:
                print(f"❌ Error: {file_path} does not contain a valid list.")
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON format in {file_path}")
    else:
        print(f"❌ Error: {file_path} not found!")

# ✅ Insert all data
insert_data(file_path_remedies, collection_remedies, "symptom")
insert_data(file_path_plants, collection_plants, "name")
insert_data(file_path_recipes, collection_recipes, "name")

print("🎯 All data insertion processes completed successfully!")
