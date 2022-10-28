from service.extensions import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    id_admin = db.Column(db.Boolean, nullable=False)
    date_joined = db.Columg(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<User(id='%s', first_name='%s', last_name='%s', email='%s', is_admin='%s', date_joined='%s', last_login='%s', password='%s')>" % (
            self.n,
            self.first_name,
            self.last_name,
            self.email,
            self.is_admin,
            self.date_joined,
            self.last_login,
            self.password,
        )

