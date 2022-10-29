from service.extensions import db

class user(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    id_admin = db.Column(db.Boolean, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    requests = db.relationship('request_pool', backref='user', lazy=True)

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
    segment_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    floor_quantity = db.Column(db.Integer, unique=False, nullable=False)
    wall_material_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    room_quantity = db.Column(db.Integer, unique=False, nullable=False)
    # reference_flat = db.Column(db.DateTime, nullable=True)
    stage = db.Column(db.Integer, nullable=False)  # ДЕЛАТЬ ИЛИ НЕ ДЕЛАТЬ ТАБЛИЦУ-СЛОВАРЬ

    def __repr__(self):
        return "<request_pool(id='%s', first_name='%s', last_name='%s', email='%s', is_admin='%s'," \
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
    total_area = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    kitchen_area = db.Column(db.Integer, unique=False, nullable=False)
    have_balcony = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    minutes_metro_walk = db.Column(db.Integer, unique=False, nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'),
                          nullable=False)
    price = db.Column(db., nullable=True)

    def __repr__(self):
        return "<request_pool(id='%s', first_name='%s', last_name='%s', email='%s', is_admin='%s'," \
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

class condition(db.Model):
    __tablename__ = "condition"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    flats = db.relationship('flat', backref='condition', lazy=True)

    def __repr__(self):
        return "<wall_material(id='%s', name='%s')>" % (
            self.id,
            self.name,
        )