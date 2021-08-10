from pdb import set_trace
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity)


from .models import get_as_dict, Room, Item

bp = Blueprint('room', __name__)


@bp.route('/api/v1.0/rooms/<int:room_id>', methods=['GET'])
# @jwt_required
def rooms(room_id):
    r = Room.query.get_or_404(room_id)
    # fields = Room.FIELD_NAMES + ['id']
    # result = get_as_dict(r, fields=fields)
    print(r)
    return jsonify(r), 200
