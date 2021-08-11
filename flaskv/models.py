import decimal

from flask_login import UserMixin
from flask import Markup

from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


CC_PREFIX = 4
CC_POSTFIX = 6


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_as_dict(model, fields=None, exclude=[]):
    ret = {}
    fields = fields or [f for f in model.FIELD_NAMES if f not in exclude]
    for field in fields:
        value = getattr(model, field)
        if isinstance(value, db.Model):
            value = str(value)
        ret[field] = value
    return ret


def get_nice_text(model, html=True, exclude=[]):
    text = ''
    newline = '<br/>' if html else '\n'
    fields = [f for f in model.FIELD_NAMES if f not in exclude]
    for field in fields:
        value = getattr(model, field)
        if type(value) is bool: value = ('No', 'Yes')[value]
        if value is None: value = 'No data'
        if type(value) is decimal.Decimal:
            value = '{:,.2f}'.format(value)
        name = field.capitalize().replace('_', ' ')
        text += '%s: %s%s' % (name, value, newline)
    return Markup(text) if html else text


class User(UserMixin, db.Model):
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    FIELD_NAMES = 'email first_name last_name'.split()

    # prevent IDE warning when creating instance
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', back_populates='user', lazy=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def nice_text(self, **kw):
        return get_nice_text(self, **kw)

    def __repr__(self):
        return '<User: %r>' % self.email


class Set(db.Model):
    __tablename__ = 'sets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    item_types = db.relationship('ItemType', back_populates='set', lazy=True)


class ItemType(db.Model):
    __tablename__ = 'item_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    img = db.relationship('Image')
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'))
    set = db.relationship('Set', back_populates='item_types')


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.SmallInteger, nullable=False)
    y = db.Column(db.SmallInteger, nullable=False)
    z = db.Column(db.SmallInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='items')
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_types.id'))
    item_type = db.relationship('ItemType')
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    room = db.relationship('Room', back_populates='items')
    # cell_id = db.relationship('Cell', db.ForeignKey('cells.id'))
    # cell = db.relationship('Cell', back_populates='item')


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    img = db.relationship('Image')
    # cells = db.relationship('Cell', back_populates='room', lazy=True)
    items = db.relationship('Item', back_populates='room', lazy=True)
    nroom_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    nroom = db.relationship('Room', uselist=False, foreign_keys=[nroom_id], remote_side=[id])
    sroom_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    sroom = db.relationship('Room', uselist=False, foreign_keys=[sroom_id], remote_side=[id])
    wroom_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    wroom = db.relationship('Room', uselist=False, foreign_keys=[wroom_id], remote_side=[id])
    eroom_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    eroom = db.relationship('Room', uselist=False, foreign_keys=[eroom_id], remote_side=[id])


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250))

'''
class Cell(db.Model):
    __tablename__ = 'cells'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.SmallInteger, nullable=False)
    y = db.Column(db.SmallInteger, nullable=False)
    is_wall = db.Column(db.Boolean, default=False)
    glyph_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', back_populates='cell')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
'''