from app.extensions import db


class Exchange(db.Model):
    __tablename__ = 'exchange'

    id = db.Column(db.Integer, primary_key=True)
    currency_from = db.Column(db.String(256))
    currency_to = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Exchange({}, currency_from={}, currency_to={} value={} date={}>'.format(self.id,
                                                                                         self.currency_from,
                                                                                         self.currency_to,
                                                                                         self.value,
                                                                                         self.date)
