from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

"""
Note return codes:
    200 = Ok
    201 = Created
    202 = Async created
    400 = Bad request
    404 = Not found
    500 = Server error
"""


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store id required"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(
                name=name,
                price=data['price'],
                store_id=data['store_id']
        )
        item.save_to_db()
        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(
                    name=name,
                    price=data['price'],
                    store_id=data['store_id']
            )
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': "Item not found"}, 401
        item.delete_from_db()
        return {'message': 'Item deleted'}, 200


class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
