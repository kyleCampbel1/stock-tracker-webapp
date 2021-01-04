from flask import Blueprint, jsonify, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .app import db 
from .views import main

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.add_metric'))

@auth.route('/signup', methods=['POST'])
def signup():
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 
    if user: 
        return jsonify({msg:'email already in use'}) 

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for(auth.login)), 201

@auth.route('/logout', methods=['POST'])
def logout():
    return 'Logout'
