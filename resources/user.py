from flask_restful import Resource, reqparse

from models.user import UserModel

"""
Note return codes:
    200 = Ok
    201 = Created
    202 = Async created
    400 = Bad request
    404 = Not found
    500 = Server error
"""


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password required"
                        )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that name already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404

        user.delete_from_db()
        return {'message': "User deleted"}, 200


