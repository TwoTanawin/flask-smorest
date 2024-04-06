from flask import Flask, request
from db import items, stores
from flask_smorest import abort
import uuid

app = Flask(__name__)



@app.get("/store") # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' are include in the Json payload")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404, message=f"Store already exists")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_items():
    item_data = request.get_json()
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400,
              message="Bad request. Ensure 'price', 'store_id', and'name' are include in the Json payload")
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(404, message=f"Item already exists")

    if item_data["store_id"] not in stores:
        # return {"message":"Stores not found"}, 404
        abort(404, message="Stores not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>") 
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message":"Stores not found"}, 404

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message":"Item not found"}, 404
    

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'name' and 'price' are include in the Json payload")  
    
    try:
        item = item_id["item_id"]
        item |= item_data

        return item
    except KeyError:
        abort(400, message="Item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items["item_id"]
        return {"message":"Item delete"}
    except KeyError:
        abort(400, message="Item not found")

@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    if "price" not in store_data or "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' and 'price' are include in the Json payload")  
    
    try:
        store = store_id["store_id"]
        store |= store_data

        return store
    except KeyError:
        abort(400, message="store not found")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores["store_id"]
        return {"message":"store delete"}
    except KeyError:
        abort(400, message="store not found")