import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models.store import StoreModel
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint(
    "store", __name__, description="Operations on stores"
)

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted."}
        except SQLAlchemyError:
            abort(500, message="Internal server error.")
        
    @blp.arguments(StoreSchema)
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
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Store already exists.")
        except SQLAlchemyError:
            abort(500, message="Internal server error.")