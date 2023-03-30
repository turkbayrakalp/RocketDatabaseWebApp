from flask import Flask
from flask_login import LoginManager

import views
from users import get_user
import database

lm = LoginManager()

@lm.user_loader
def load_user(username):
    return get_user(username)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DummyKey'

    # now we register the blueprints
    app.register_blueprint(views.views, url_prefix = '/')

    app.config["user-db"] = "user-data.db"

    lm.init_app(app)
    lm.login_view = "views.login"

    # Set latest IDs for insertable tables

    capsule_id = -1
    for capsule in database.get_capsules():
        current_id = capsule["capsule_id"]
        if current_id.isdigit():
            if int(current_id) > int(capsule_id):
                capsule_id = current_id
    app.config["capsule_id"] = int(capsule_id) + 1

    launch_id = -1
    for launch in database.get_launches():
        current_id = launch["launch_id"]
        if current_id.isdigit():
            if int(current_id) > int(launch_id):
                launch_id = current_id
    app.config["launch_id"] = int(launch_id) + 1

    payload_id = -1
    for payload in database.get_payloads():
        current_id = payload["payload_id"]
        if current_id.isdigit():
            if int(current_id) > int(payload_id):
                payload_id = current_id
    app.config["payload_id"] = int(payload_id) + 1
    
    rocket_id = -1
    for rocket in database.get_rockets():
        current_id = rocket["rocket_id"]
        if current_id.isdigit():
            if int(current_id) > int(rocket_id):
                rocket_id = current_id
    app.config["rocket_id"] = int(rocket_id) + 1
    
    core_id = -1
    for core in database.get_cores():
        current_id = core["core_id"]
        if current_id.isdigit():
            if int(current_id) > int(core_id):
                core_id = current_id
    app.config["core_id"] = int(core_id) + 1

    ship_id = -1
    for ship in database.get_ships():
        current_id = ship["ship_id"]
        if current_id.isdigit():
            if int(current_id) > int(ship_id):
                ship_id = current_id
    app.config["ship_id"] = int(ship_id) + 1
    # Other configs (hardcoded - could be avoided if launched as `cd website´):
    #   database.py (db_location)
    #   database ( open("/static/rocket_images/"... )
    #   users.py (user_db_location)

    return app