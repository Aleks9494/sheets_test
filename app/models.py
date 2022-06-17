from app import db


class MyModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer(), primary_key=True)
    order_number = db.Column(db.Integer(), nullable=False)
    cost_dollar = db.Column(db.Float(), nullable=False)
    cost_rubles = db.Column(db.Float(), nullable=False)
    order_date = db.Column(db.String(), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
