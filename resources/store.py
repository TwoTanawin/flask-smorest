from flask import Flask, request
from db import items, stores
from flask_smorest import Blueprint, abort
import uuid
from flask.views import MethodView


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            store = store_id["store_id"]
            return store
        except KeyError:
            abort(400, message="store not found")

    def delete(self, store_id):
        try:
            del stores["store_id"]
            return {"message":"store delete"}
        except KeyError:
            abort(400, message="store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}
    
    def post(self):
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