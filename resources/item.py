from flask import Flask, request
from db import items, stores
from flask_smorest import Blueprint, abort
import uuid
from flask.views import MethodView

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return {"message":"Item not found"}, 404

    def delete(self, item_id):
        try:
            del items["item_id"]
            return {"message":"Item delete"}
        except KeyError:
            abort(400, message="Item not found")

    def put(self, item_id):
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

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.json
        if not item_data or "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload")

        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, message="Item already exists")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201