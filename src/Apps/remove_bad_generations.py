from src.Databases.MJDB import get_database

# connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

query = {
"tags": {
"$regex": '^[a-zA-Z0-9]',
"$options" :'i' # case-insensitive
}
}

items = collection_name.find(query)

for item in items:
    print(item)
count = collection_name.count_documents(query)
print(count)

response = input("Does this look good (yes or no): ")
if response == "no":
    print("stopping")
elif response == "yes":
    print("removing entries")
    collection_name.delete_many(query)
else:
    print("bad answer, stopping")
