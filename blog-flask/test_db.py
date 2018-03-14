from routes import test_db as test_db_routes
from app_db import app

from routes.test_db import main as test_db_routes

#app = Flask (__name__)

#app.config.from_object('config')
#db = SQLAlchemy(app)
app.register_blueprint(test_db_routes,url_prefix = '/cust_db')


if __name__ == '__main__':

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
