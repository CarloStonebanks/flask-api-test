from flask_restful import Resource, Api, reqparse
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store '{}' already exists".format(name)}, 400

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred creating the store"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': "An error occurred deleting the store"}, 500

        return {'message': "Store deleted"}, 200


class StoreList(Resource):

    def get(self):
        return {
            'stores': [store.json() for store in StoreModel.find_all()]
        }, 200
