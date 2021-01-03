from .app import db 

class Metric(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # give fields in accordance with what we query from cryptowatch
    close_time = db.Column(db.String(20))
    open_price = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    volume_quote = db.Column(db.Float)