from .models import Metric, User, Markets, tags
from .app import db, create_app

db.create_all(app=create_app())