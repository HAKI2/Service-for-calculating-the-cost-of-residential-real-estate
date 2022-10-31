import datetime

from service.extensions import db


class user(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    last_login = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    requests = db.relationship('request_pool', backref='user', lazy=True, cascade="all, delete")

    def __repr__(self):
        return "<User(id='%s', first_name='%s', last_name='%s', email='%s', is_admin='%s'," \
               " date_joined='%s', last_login='%s', password='%s')>" % (
                   self.n,
                   self.first_name,
                   self.last_name,
                   self.email,
                   self.is_admin,
                   self.date_joined,
                   self.last_login,
                   self.password,
               )


class request_pool(db.Model):
    __tablename__ = "request_pool"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    location = db.Column(db.String(80), unique=False, nullable=False)
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'),
                           nullable=False)
    floor_quantity = db.Column(db.Integer, unique=False, nullable=False)
    wall_material_id = db.Column(db.Integer, db.ForeignKey('wall_material.id'),
                                 nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    stage = db.Column(db.Integer, nullable=False, default=1)
    flats = db.relationship('flat', backref='request_pool', lazy=True, cascade="all, delete")

    def __repr__(self):
        return "<request_pool(id='%s', user_id='%s', location='%s', segment_id='%s', floor_quantity='%s'," \
               " wall_material_id='%s', room_quantity='%s', stage='%s')>" % (
                   self.id,
                   self.user_id,
                   self.location,
                   self.segment_id,
                   self.floor_quantity,
                   self.wall_material_id,
                   self.room_quantity,
                   self.stage,
               )


class segment(db.Model):
    __tablename__ = "segment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    buildings = db.relationship('request_pool', backref='segment', lazy=True)

    def __repr__(self):
        return "<segment(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class wall_material(db.Model):
    __tablename__ = "wall_material"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    buildings = db.relationship('request_pool', backref='wall_material', lazy=True)

    def __repr__(self):
        return "<wall_material(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class flat(db.Model):
    __tablename__ = "flat"
    id = db.Column(db.Integer, primary_key=True)
    request_pool_id = db.Column(db.Integer, db.ForeignKey('request_pool.id'),
                                nullable=False)
    floor = db.Column(db.Integer, unique=False, nullable=False)
    room_quantity = db.Column(db.Integer, unique=False, nullable=False)
    total_area = db.Column(db.Float, nullable=False)
    kitchen_area = db.Column(db.Float, unique=False, nullable=False)
    have_balcony = db.Column(db.Boolean, nullable=False)
    minutes_metro_walk = db.Column(db.Integer, unique=False, nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'),
                             nullable=False)
    price = db.Column(db.Numeric(precision=22, scale=10), nullable=True)
    is_reference = db.Column(db.Boolean, nullable=False, default=False)
    analogue_flats = db.relationship('analogue_flat', backref='flat', lazy=True, cascade="all, delete")

    def __repr__(self):
        return "<flat(id='%s', request_pool_id='%s', floor='%s', total_area='%s', kitchen_area='%s'," \
               " have_balcony='%s', minutes_metro_walk='%s', condition_id='%s', price='%s', room_quantity='%s')>" % (
                   self.id,
                   self.request_pool_id,
                   self.floor,
                   self.total_area,
                   self.kitchen_area,
                   self.have_balcony,
                   self.minutes_metro_walk,
                   self.condition_id,
                   self.price,
                   self.room_quantity,
               )


class condition(db.Model):
    __tablename__ = "condition"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    flats = db.relationship('flat', backref='condition', lazy=True)
    analogue_flats = db.relationship('analogue_flat', backref='condition', lazy=True)

    def __repr__(self):
        return "<condition(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )


class analogue_flat(db.Model):
    __tablename__ = "analogue_flat"
    id = db.Column(db.Integer, primary_key=True)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'),
                        nullable=False)
    location = db.Column(db.String(80), unique=False, nullable=False)
    floor = db.Column(db.Integer, unique=False, nullable=False)
    total_area = db.Column(db.Float, nullable=False)
    kitchen_area = db.Column(db.Float, unique=False, nullable=False)
    have_balcony = db.Column(db.Boolean, nullable=False)
    minutes_metro_walk = db.Column(db.Integer, unique=False, nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'),
                             nullable=False)
    price = db.Column(db.Numeric(precision=22, scale=10), nullable=True)
    is_ignored = db.Column(db.Boolean, nullable=False, default=False)
    analogue_flat_corr = db.relationship('analogue_flat_corr', backref='analogue_flat', lazy=True,
                                         cascade="all, delete")

    def __repr__(self):
        return "<analogue_flat(id='%s', flat_id='%s', location='%s', floor='%s', total_area='%s', kitchen_area='%s'," \
               " have_balcony='%s', minutes_metro_walk='%s', condition_id='%s', price='%s', is_ignored='%s')>" % (
                   self.id,
                   self.flat_id,
                   self.location,
                   self.floor,
                   self.total_area,
                   self.kitchen_area,
                   self.have_balcony,
                   self.minutes_metro_walk,
                   self.condition_id,
                   self.price,
                   self.is_ignored
               )


class analogue_flat_corr(db.Model):
    __tablename__ = "analogue_flat_corr"
    id = db.Column(db.Integer, primary_key=True)
    analogue_flat_id = db.Column(db.Integer, db.ForeignKey('analogue_flat.id'),
                                 nullable=False)
    location_corr = db.Column(db.Float, unique=False, nullable=False)
    floor_corr = db.Column(db.Float, unique=False, nullable=False)
    total_area_corr = db.Column(db.Float, nullable=False)
    kitchen_area_corr = db.Column(db.Float, unique=False, nullable=False)
    have_balcony_corr = db.Column(db.Float, nullable=False)
    minutes_metro_walk_corr = db.Column(db.Float, unique=False, nullable=False)
    condition_corr = db.Column(db.Integer, nullable=False)
    price_corr = db.Column(db.Numeric(precision=22, scale=10), nullable=False)
    is_ignored = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<analogue_flat_corr(id='%s', analogue_flat_id='%s', location_corr='%s', floor_corr='%s'," \
               " total_area_corr='%s', kitchen_area_corr='%s', have_balcony_corr='%s', minutes_metro_walk_corr='%s'," \
               "  condition_corr='%s', price_corr='%s', is_ignored='%s')>" % (
                   self.id,
                   self.analogue_flat_id,
                   self.location_corr,
                   self.floor_corr,
                   self.total_area_corr,
                   self.kitchen_area_corr,
                   self.have_balcony_corr,
                   self.minutes_metro_walk_corr,
                   self.condition_corr,
                   self.price_corr,
                   self.is_ignored
               )
