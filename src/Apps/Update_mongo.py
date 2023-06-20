from bson import ObjectId
from src.Databases.MJDB import get_database
from pymongo.errors import PyMongoError
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bucket', type=str, help='Where are we uploading')
parser.add_argument('--filename', type=str, help='Where are we uploading')
args = parser.parse_args()
bucket = args.bucket
filename = args.filename

#bucket = "Redbubble"
#filename = "ObjectId6490a3e8e9c65fa34b98542c_Germanium_Optical_Illusion_Patterns_Cross_Squares_in_Grid_Jn_Hung_Gold_Tibetan_Yellow_Beechwood_Giant_Onion_3D_Anamorphic_Drawing_20794d6e-0ef0-11ee-aead-8c1d96ef2d9b.png"

# connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

object_value = filename.split("_")
print(object_value)
mongo_id_hex = object_value[0].lstrip("ObjectId")
print(mongo_id_hex)
mongo_id = ObjectId(mongo_id_hex)
print(mongo_id)

item = collection_name.find({"_id": mongo_id})



for item in item:
    if "PoD-sites" in item:
        if bucket in item["PoD-sites"]:
            print("already exists")
        else:
            try:
                result = collection_name.update_one({"_id": mongo_id}, {'$push': {'PoD-sites': bucket}})
                if result.modified_count == 0:
                    print("No documents were updated")
                else:
                    print(f"{result.modified_count} documents were updated")
            except PyMongoError as e:
                print(f"An error occurred: {str(e)}")
    else:
        try:
            result = collection_name.update_one({"_id": mongo_id}, {'$push': {'PoD-sites': bucket}})
            if result.modified_count == 0:
                print("No documents were updated")
            else:
                print(f"{result.modified_count} documents were updated")
        except PyMongoError as e:
            print(f"An error occurred: {str(e)}")
