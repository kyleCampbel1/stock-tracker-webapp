from .app import db 

tags = db.Table('tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('market_id', db.Integer, db.ForeignKey('markets.id'), primary_key=True)
)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100), db.ForeignKey('market.ticker'), nullable=False)
    # give fields in accordance with what we query from cryptowatch
    close_time = db.Column(db.DateTime)
    open_price = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    volume_quote = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    tags = db.relationship('Markets', secondary=tags, lazy='subquery', backref=db.backref('users', lazy=True))

class Markets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100))
    metrics = db.relationship('Metric', backref='market', lazy=True)
