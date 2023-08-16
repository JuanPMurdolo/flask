import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from RestAPI.schemas import ItemSchema, ItemUpdateSchema
from db import items


blp = Blueprint(
    "item", __name__, description="Operations on items"
)

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id: str):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message ="Store not found")

    def delete(self, item_id: str):
        try:
            del items[item_id]
            return {"message": "Store deleted."}
        except KeyError:
            return abort(404, message="Store not found.")
        
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
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
            )
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item