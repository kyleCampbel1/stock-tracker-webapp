# from flask import Blueprint, jsonify, redirect, url_for, request, flash, session, g
# from werkzeug.security import generate_password_hash, check_password_hash
# from .app import db 
# from .views import main

# auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = User.query.filter_by(email=email).first()

#     if not user or not check_password_hash(user.password, password):
#         error = 'Incorrect credentials'
#     if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('main.add_metric'))
#     # if the above check passes, then we know the user has the right credentials
#     flash(error)
#     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

# @auth.route('/signup', methods=['POST'])
# def signup():

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()
#     return redirect(url_for('auth.login'))
#     if not username:
#         error = 'Username is required.'
#     elif not password:
#         error = 'Password is required.'
#     elif db.execute(
#         'SELECT id FROM user WHERE username = ?', (username,)
#     ).fetchone() is not None:
#         error = 'User {} is already registered.'.format(username)

#     if error is None:
#         new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('auth.login'))

#     flash(error)

#     return redirect(url_for('auth.signup'))

# @auth.route('/logout', methods=['POST'])
# def logout():
#     session.clear()
#     return redirect(url_for('auth.login'))

# @auth.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

#     return 

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view