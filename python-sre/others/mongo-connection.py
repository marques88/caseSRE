from pymongo import MongoClient


def filter_by_item(obj):
    item_to_query = {"_id": obj["_id"]}
    items = database.inventory.find(item_to_query)
    return obj not in items


mongo_client = MongoClient("127.0.0.1")
database = mongo_client.dbtutorial

print(f"Database list: {mongo_client.list_database_names()}")
print(f"Collections names: {database.list_collection_names()}")

invetory_data = [
    {
        "_id": "journal",
        "item": "journal",
        "qty": 25,
        "tags": ["blank", "red"],
        "dim_cm": [14, 21],
    },
    {
        "_id": "notebook",
        "item": "notebook",
        "qty": 50,
        "tags": ["red", "blank"],
        "dim_cm": [14, 21],
    },
    {
        "_id": "paper",
        "item": "paper",
        "qty": 100,
        "tags": ["red", "blank", "plain"],
        "dim_cm": [14, 21],
    },
    {
        "_id": "planner",
        "item": "planner",
        "qty": 75,
        "tags": ["blank", "red"],
        "dim_cm": [22.85, 30],
    },
    {
        "_id": "postcard",
        "item": "postcard",
        "qty": 45,
        "tags": ["blue"],
        "dim_cm": [10, 15.25],
    },
    {
        "_id": "scrapbook",
        "item": "scrapbook",
        "qty": 45,
        "tags": ["purple", "red"],
        "dim_cm": [5, 5],
    },
]

database.inventory.delete_one({ "_id": "scrapbook"})

filter_result = filter(filter_by_item, invetory_data)
new_items_to_insert = []
print("========== items not in inventory ===========")
for filtered_item in filter_result:
    new_items_to_insert.append(filtered_item)

if len(new_items_to_insert) > 0:
    inserted_items = database.inventory.insert_many(new_items_to_insert)
    print(f"{len(inserted_items.inserted_ids)} documents inserted.")    
else:
    print("no items to insert")

print("****** finding journal item in database ******")
item_query = {"item": "journal"}
for z in database.inventory.find(
    item_query,
):
    print(z)

print("========== items in inventory ===========")
for z in database.inventory.find():
    print(z)

# database.inventory.drop()
