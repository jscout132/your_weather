from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
marsh = Marshmallow()
sqla = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(sqla.Model, UserMixin):
    id = sqla.Column(sqla.String, primary_key=True)
    email = sqla.Column(sqla.String(150), nullable=False, default='')
    password = sqla.Column(sqla.String, nullable=False, default='')
    user_city = sqla.Column(sqla.String(150), nullable=True, default='')
    f_name = sqla.Column(sqla.String(150), nullable=True, default='')
    l_name = sqla.Column(sqla.String(150), nullable=True, default='')
    date_created = sqla.Column(sqla.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, email='', password='', user_city='', f_name='', l_name=''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.user_city = user_city
        self.f_name = f_name
        self.l_name = l_name

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)
        return self.pass_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'
    


class FavoriteCities(sqla.Model, UserMixin):
    id = sqla.Column(sqla.String(50), nullable = False, primary_key=True)
    city = sqla.Column(sqla.String(150), nullable = True, default='')
    user_id = sqla.Column(sqla.String, sqla.ForeignKey('user.id'))

    def __init__(self, city='', user_id=''):
        self.id = self.set_id()
        self.city = city
        self.user_id = user_id

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return self.city

class CitySchema(marsh.Schema):
    class Meta:
        fields = [
            'id',
            'city',
            'user_id'
        ]

city_schema = CitySchema()
cities_schema = CitySchema(many = True)