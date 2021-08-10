
from flask import Blueprint, request, jsonify

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity)

# import the instance created in __init__.py
from . import limiter
from .models import db, User

bp = Blueprint('auth', __name__)

MAX_USERNAME = 128
MAX_PASSWORD = 256


@bp.route('/api/v1.0/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    user_id = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=user_id)
    }
    return jsonify(ret), 200


@bp.route('/api/v1.0/fresh-login', methods=['POST'])
def fresh_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=username).first()

    if user and user.verify_password(password):
        user_id = str(user.id)
        ret = {
            'access_token': create_access_token(identity=user_id, fresh=True),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return jsonify(ret), 200

    return jsonify({"msg": "Bad username or password"}), 401


@bp.route('/api/v1.0/change-pwd', methods=['GET'])
@jwt_required(fresh=True)
def protected_fresh():
    username = get_jwt_identity()
    return jsonify(fresh_logged_in_as=username), 200


@bp.route('/api/v1.0/register', methods=['POST'])
@limiter.limit('1/minute; 10/day')
def api_register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    first_name = request.json.get('first_name', None)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or len(username) > MAX_USERNAME:
        return jsonify({"msg": "Bad or missing username parameter"}), 400
    if not password or len(password) > MAX_PASSWORD:
        return jsonify({"msg": "Bad or missing password parameter"}), 400

    user = User.query.filter_by(email=username).first()
    if user:
        return jsonify({"msg": "User already exists"}), 409

    first_name = first_name or username.split('@')[0] or username
    user = User(email=username, first_name=first_name, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "You have successfully registered"}), 200


@bp.route('/api/v1.0/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=username).first()

    if user and user.verify_password(password):
        user_id = str(user.id)
        ret = {
            'access_token': create_access_token(identity=user_id),
            'refresh_token': create_refresh_token(identity=user_id),
            'email' : user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return jsonify(ret), 200

    return jsonify({"msg": "Bad username or password"}), 401


@bp.route('/api/v1.0/test', methods=['GET'])
def test():
    return jsonify({"msg": "ok"}), 200
