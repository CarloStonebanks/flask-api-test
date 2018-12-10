import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

"""
Note return codes:
    200 = Ok
    201 = Created
    202 = Async created
    400 = Bad request
    404 = Not found
"""

app = Flask(__name__)
app.secret_key = 'carlo'

# Turns off Flask SQLAlchemy feature, favoring SQLAlchemy's own which is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///data.db'
)
# Allow Flask to expose errors to client instead of being trapped by PyCharm
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__' :
    # Avoid other package imports of db causing circular imports
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
