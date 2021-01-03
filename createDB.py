from api.metric import Metric
from api.app import db, create_app

db.create_all(app=create_app())