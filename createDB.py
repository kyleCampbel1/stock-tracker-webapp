from api.models import Metric, User, Markets, tags
from api.app import db, create_app

db.create_all(app=create_app())