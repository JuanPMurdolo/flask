import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint(
    "item", __name__, description="Operations on items"
)

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id: str):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id: str):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted."}
        except SQLAlchemyError:
            abort(500, message="Internal server error.")
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request. Ensure 'price' is included in the JSON payload.",
            )
        try:
            item = items[item_id]
            item != item_data
            return item
        except KeyError:
            return abort(404, message="Item not found.")
        
@blp.route("/item")
class ItemList(MethodView):  
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return {'items': list(items.values())}

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data): 
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Internal server error.")
        return item