from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from .site.routes import site
from .authentication.routes import auth
from .api.open_weather import open_weather
from config import Config
from models import marsh, sqla, login_manager
from helpers import Encoding

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
	app.run(debug=True)

app.register_blueprint(site)
app.register_blueprint(auth)

app.register_blueprint(open_weather)

app.json_encoder = Encoding

app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'
sqla.init_app(app)
login_manager.init_app(app)
marsh.init_app(app)
migrate = Migrate(app, sqla)