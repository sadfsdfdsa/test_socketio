from flask import Flask, render_template
from database.database import Database
from config.config import Config

# custom app settings for REST API and frontend on vue
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='static')

app.config.from_object(Config)

# Database init
db = Database("db.db")
db.create_tables()

# DO NOT DELETE OR MOVE ON TOP
# import routes
from routes.User import *


# frontend index page
@app.route('/')
def index():
    return render_template('index.html')


# give all to vue router
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
