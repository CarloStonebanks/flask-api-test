from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # Because ItemModel declared a foreign key column, a one to many model
    # to Items is assumed
    # lazy=dynamic tells the relationship to not actually render the objects
    # (for performance reasons) until we retrieve via .all()
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.id = None
        self.name = name
        self.items = []

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        """
        :param name:
        :type: str
        :return:
        :rtype: StoreModel
        """
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
