from pdb import set_trace
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity)


from .models import get_as_dict, Room, Item

bp = Blueprint('room', __name__)


@bp.route('/api/v1.0/rooms/<int:room_id>', methods=['GET'])
# @jwt_required
def rooms(room_id):
    print(f'*** room_id={room_id}\n')
    r = Room.query.get_or_404(room_id)
    items = []
    for i in r.items:
        d = dict(id=i.id, name=i.item_type.name, x=i.x, y=i.y,z=i.z, img='assets/'+i.item_type.img.path)
        items.append(d)
    result = dict(img='assets/'+r.img.path, items=items)
    print(result)
    return jsonify(result), 200
