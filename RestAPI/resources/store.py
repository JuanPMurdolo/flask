import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from RestAPI.schemas import StoreSchema, StoreUpdateSchema
from db import stores

blp = Blueprint(
    "store", __name__, description="Operations on stores"
)

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message ="Store not found")

    def delete(self, store_id: str):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            return abort(404, message="Store not found.")
        
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store != store_data
            return store
        except KeyError:
            return abort(404, message="Store not found.")

@blp.route("/store")  
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) 
    def get(self):
        return {'stores': list(stores.values())}

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, 'id': store_id}
        stores[store_id] = new_store
        return new_store, 201