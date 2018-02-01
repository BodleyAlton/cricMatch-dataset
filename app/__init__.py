from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from gevent.wsgi import WSGIServer

app=Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://altonbodley@127.0.0.1/matchStats"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
db=SQLAlchemy(app)

# http_server = WSGIServer(('', 8080), app)
# http_server.serve_forever()

from app import views