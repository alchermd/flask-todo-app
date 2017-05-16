from flask import Flask

app = Flask(__name__)
from app import views

# Flask configuration
app.config.from_object(__name__)
app.config.update(dict(
    MYSQL_HOST='localhost',
    MYSQL_USER='root',
    MYSQL_PASSWORD='123456',
    MYSQL_DB='flask_todo_app',
    MYSQL_CURSORCLASS='DictCursor',
    SECRET_KEY='development key'
))