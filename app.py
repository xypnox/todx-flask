import os
from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from todx import __version__

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index_handle():
    return jsonify({'Todx': __version__})

@app.route('/login', methods=['POST'])
def login_handle():
    if current_user.is_authenticated:
        return make_response(jsonify({'login': 'True', 'username': current_user.username}), 202)
    if not request.json or not 'username' in request.json:
        return make_response(jsonify({'error': 'BAD REQUEST'}), 400)

    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return make_response(jsonify({'error': 'User Password Not match'}), 401)
    login_user(user)
    return make_response(jsonify({'login': 'True', 'username': current_user.username}), 202)



@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return make_response(jsonify({'login': 'True', 'username': current_user.username}), 202)
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None:
        user = User(username=request.json['username'])
        user.set_password(request.json['password'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'register': 'True'}), 202)
    return make_response(jsonify({'register': 'False'}), 401)


@app.route('/upload', methods=['POST'])
@login_required
def upload_route():
    print(current_user.username)
    user = User.query.filter_by(username=current_user.username).first()
    user.todxdata = request.json['todxdata']
    print(user.todxdata)
    db.session.commit()
    return make_response(jsonify({'todxdata': 'saved'}), 202)

@app.route('/download', methods=['GET'])
@login_required
def download_route():
    user = User.query.filter_by(username=current_user.username).first()
    print(user.todxdata)
    return make_response(jsonify({'todxdata': user.todxdata}), 202)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/logout')
def logout():
    logout_user()
    return make_response(jsonify({'logout': 'True'}), 202)

if __name__ == '__main__':
    # this should be at the top but it causes circular imports
    # so it is at the bottom
    from models import User 
    app.run()

