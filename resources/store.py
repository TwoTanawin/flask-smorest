from flask import Flask, request
from db import items, stores
from flask_smorest import Blueprint, abort
import uuid
from flask.views import MethodView
from schemas import StoreSchema


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
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store