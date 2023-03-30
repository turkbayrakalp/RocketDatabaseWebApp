# This file is for arranging which pages the user can navigate to (i.e. launchpads, launches, rockets, ships...) #
# This file is a blueprint, it has a bunch of roots and urls inside of it #

from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

import passlib.hash

import forms
import database
import users

views = Blueprint('views', __name__)

@views.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = users.get_user(username)

        if user is None:
            password = form.data["password"]
            hashed_password = \
                passlib.hash.pbkdf2_sha256.hash(password)

            user_type = "regular"
            deserves_adminhood = True if form.data["superfan"] == "True" else False
            if deserves_adminhood and "wants_admin" in request.form.keys():
                user_type = "admin"

            users.add_user(username, hashed_password, user_type)

            flash("You're all set, you can log in.")
            return redirect(url_for("views.login"))
        else:
            flash("That username is taken, please choose another.")
    
    return render_template("signup.html", form=form)

@views.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = users.get_user(username)

        if user is not None:
            password = form.data["password"]
            if passlib.hash.pbkdf2_sha256.verify(password, user.password):
                login_user(user)
                flash("Welcome to SpaceXhibit!")

                return redirect(url_for("views.home"))
            else:
                flash("Wrong password.")
        else:
            flash("You're not on the guest list. Why don't you sign up?")
    
    return render_template("login.html", form=form)

@views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@views.route('/home')
@views.route("/")
def home():
    return render_template("home.html")

# Capsules
@views.route('/capsules', methods=['GET', 'POST'])
def capsules():
    capsule_data = database.get_capsules()
    return render_template("capsules.html", capsules=capsule_data)

@views.route("/add_capsule", methods=["POST"])
def add_capsule():
    database.add_capsule(request)
    return redirect(url_for("views.capsules"))

@views.route('/delete_capsule', methods=['GET'])
def delete_capsule():
    database.delete_capsule(request.args.get("capsule_id"))
    return redirect(url_for("views.capsules"))

@views.route('/update_capsule', methods=['POST'])
def update_capsule():
    database.update_capsule(request)
    return redirect(url_for("views.capsules"))

# Cores
@views.route('/cores', methods=['GET', 'POST'])
def cores():
    core_data = database.get_cores()
    return render_template("cores.html", cores=core_data, core_form = forms.CoresForm())
    
@views.route("/add_core", methods=["POST"])
@login_required
def add_core():
    if current_user.is_admin:
        database.add_core(request)
    return redirect(url_for("views.cores"))

@views.route('/delete_core', methods=['GET'])
@login_required
def delete_core():
    if current_user.is_admin:
        database.delete_core(request.args.get("core_id"))
    return redirect(url_for("views.cores"))

@views.route("/update_core", methods=["POST"])
@login_required
def update_core():
    if current_user.is_admin:
        database.update_core(request)
    return redirect(url_for("views.cores"))

@views.route('/filter_core', methods=['GET', 'POST'])
def filter_core():
    filter_core_data = database.filter_core(request)
    return render_template("cores.html", cores=filter_core_data, core_form = forms.CoresForm())

# Launches
@views.route('/launches', methods=['GET', 'POST'])
def launches():
    launch_data = database.get_launches()
    launch_details = database.get_launch_details()

    inexistent_launch_detail = []
    inexistent_launch_detail_dict = []

    rocket_data = database.get_rockets()
    rocket_dict = {}
    for rocket in rocket_data:
        rocket_dict[rocket["rocket_id"]] = rocket["name"].replace(" ", " ")
    
    launchpad_data = database.get_launchpads()
    launchpad_dict = {}
    for launchpad in launchpad_data:
        launchpad_dict[launchpad["launchpad_id"]] = launchpad["name"]

    ship_data = database.get_ships_only()
    ship_dict = {}
    for ship in ship_data:
        ship_dict[ship["ship_id"]] = ship["name"]
    
    capsule_data = database.get_capsules()
    capsule_dict = {}
    for capsule in capsule_data:
        capsule_dict[capsule["capsule_id"]] = capsule["serial"]

    present = False
    for launch in launch_data:
        for launch_detail in launch_details:
            if launch["launch_id"] == launch_detail["launch_id"]:
                present = True
                break
        if not present:
            inexistent_launch_detail += [launch["launch_id"]]
            inexistent_launch_detail_dict += [{"launch_id": launch["launch_id"], "name": launch["name"]}]
        present = False

    launch_data = database.get_launches()
    return render_template("launches.html", launches=launch_data, launch_details = launch_details,
    inexistent_launch_detail=inexistent_launch_detail,inexistent_launch_detail_dict=inexistent_launch_detail_dict,
    formM=forms.LaunchForm(), formD=forms.LaunchDetailForm(),
    rockets=rocket_dict, launchpads = launchpad_dict, ships = ship_dict, capsules = capsule_dict)

@views.route("/add_launch", methods=["POST"])
def add_launch():
    database.add_launch(request)
    return redirect(url_for("views.launches"))

@views.route('/add_launch_detail', methods=['POST'])
def add_launch_detail():
    database.add_launch_details(request)
    return redirect(url_for("views.launches"))

@views.route('/delete_launch', methods=['GET'])
def delete_launch():
    database.delete_launch(request.args.get("launch_id"))
    return redirect(url_for("views.launches"))

@views.route('/delete_launch_detail', methods=['GET'])
def delete_launch_detail():
    database.delete_launch_details(request.args.get("launch_id"))
    return redirect(url_for("views.launches"))

@views.route('/update_launch', methods=['POST'])
def update_launch():
    database.update_launch(request)
    return redirect(url_for("views.launches"))

@views.route('/update_launch_detail', methods=['POST'])
def update_launch_detail():
    database.update_launch_detail(request)
    return redirect(url_for("views.launches"))

@views.route('/launches_filtered', methods=['GET', 'POST'])
def launches_filtered():
    filter_data = database.filter_launches(request)
    return render_template("launches.html", launches=filter_data, formM=forms.LaunchForm())

# Launchpads
@views.route('/launchpads', methods=['GET'])
def launchpads():
    launchpad_data = database.get_launchpads()
    return render_template("launchpads.html", launchpads=launchpad_data)

# Payloads
@views.route('/payloads', methods=['GET'])
def payloads():
    payload_data = database.get_payloads()
    return render_template("payloads.html", payloads=payload_data, formM=forms.PayloadForm())

@views.route('/payloads_filtered', methods=['GET', 'POST'])
def payloads_filtered():
    filter_data = database.filter_payloads(request)
    return render_template("payloads.html", payloads=filter_data, formM=forms.PayloadForm())


@views.route('/add_payload', methods=['POST'])
@login_required
def add_payload():
    database.add_payload(request)
    return redirect(url_for("views.payloads" ))

@views.route("/update_payload", methods=["POST"])
def update_payload():
    database.update_payload(request)
    return redirect(url_for("views.payloads"))

@views.route('/delete_payload', methods=['GET'])
@login_required
def delete_payload():
    if current_user.is_admin:
        database.delete_payload(request.args.get("payload_id"))
    else:
        flash("Please do not poke around the exhibit.")
    return redirect(url_for("views.payloads"))

# Rockets
@views.route('/rockets', methods=['GET', 'POST'])
def rockets():
    rocket_data = database.get_rockets()
    rocket_d1_data = database.get_rocket_d1()
    rocket_d2_data = database.get_rocket_d2()
    rocket_image_data = database.get_rocket_image()

    inexistent_rocket_d1 = []
    inexistent_rocket_d2 = []
    inexistent_rocket_image = []
    inexistent_rocket_d1_dict = []
    inexistent_rocket_d2_dict = []
    inexistent_rocket_image_dict = []

    present = False
    for rocket in rocket_data:
        for rocket_d1 in rocket_d1_data:
            if rocket["rocket_id"] == rocket_d1["rocket_id"]:
                present = True
                break
        if not present:
            inexistent_rocket_d1 += [rocket["rocket_id"]]
            inexistent_rocket_d1_dict += [{"rocket_id": rocket["rocket_id"], "name": rocket["name"]}]
        present = False

        for rocket_d2 in rocket_d2_data:
            if rocket["rocket_id"] == rocket_d2["rocket_id"]:
                present = True
                break
        if not present:
            inexistent_rocket_d2 += [rocket["rocket_id"]]
            inexistent_rocket_d2_dict += [{"rocket_id": rocket["rocket_id"], "name": rocket["name"]}]
        present = False
        
        for rocket_image in rocket_image_data:
            if rocket["rocket_id"] == rocket_image["rocket_id"]:
                present = True
                break
        if not present:
            inexistent_rocket_image += [rocket["rocket_id"]]
            inexistent_rocket_image_dict += [{"rocket_id": rocket["rocket_id"], "name": rocket["name"]}]
        present = False

    return render_template("rockets.html", rockets=rocket_data,
        rocket_d1s=rocket_d1_data, rocket_d2s=rocket_d2_data, rocket_images=rocket_image_data,
        inexistent_d1=inexistent_rocket_d1, inexistent_d2=inexistent_rocket_d2, inexistent_image=inexistent_rocket_image,
        inexistent_d1_dict=inexistent_rocket_d1_dict, inexistent_d2_dict=inexistent_rocket_d2_dict, inexistent_image_dict=inexistent_rocket_image_dict,
        formM=forms.RocketForm(), formD1=forms.RocketD1Form(), formD2=forms.RocketD2Form(), formI=forms.RocketImageForm())

@views.route("/add_rocket", methods=["POST"])
def add_rocket():
    form = forms.RocketForm()
    if form.validate_on_submit():
        database.add_rocket(request)
    return redirect(url_for("views.rockets"))
@views.route('/add_rocket_detail_1', methods=['POST'])
def add_rocket_detail_1():
    form = forms.RocketD1Form()
    if form.validate_on_submit():
        database.add_rocket_d1(request)
    return redirect(url_for("views.rockets"))
@views.route('/add_rocket_detail_2', methods=['POST'])
def add_rocket_detail_2():
    form = forms.RocketD2Form()
    if form.validate_on_submit():
        database.add_rocket_d2(request)
    return redirect(url_for("views.rockets"))
@views.route('/add_rocket_image', methods=['POST'])
def add_rocket_image():
    form = forms.RocketImageForm()
    if form.validate_on_submit():
        database.add_rocket_image(request)
    return redirect(url_for("views.rockets"))

@views.route("/update_rocket", methods=["POST"])
def update_rocket():
    form = forms.RocketForm()
    if form.validate_on_submit():
        database.update_rocket(request)
    return redirect(url_for("views.rockets"))
@views.route('/update_rocket_detail_1', methods=['POST'])
def update_rocket_detail_1():
    form = forms.RocketD1Form()
    if form.validate_on_submit():
        database.update_rocket_d1(request)
    return redirect(url_for("views.rockets"))
@views.route('/update_rocket_detail_2', methods=['POST'])
def update_rocket_detail_2():
    form = forms.RocketD2Form()
    if form.validate_on_submit():
        database.update_rocket_d2(request)
    return redirect(url_for("views.rockets"))

@views.route('/delete_rocket', methods=['GET'])
@login_required
def delete_rocket():
    if current_user.is_admin:
        database.delete_rocket(request.args.get("rocket_id"))
    else:
        flash("Please do not poke around the exhibit.")
    return redirect(url_for("views.rockets"))
@views.route('/delete_rocket_detail_1', methods=['GET'])
def delete_rocket_detail_1():
    database.delete_rocket_d1(request.args.get("rocket_id"))
    return redirect(url_for("views.rockets"))
@views.route('/delete_rocket_detail_2', methods=['GET'])
def delete_rocket_detail_2():
    database.delete_rocket_d2(request.args.get("rocket_id"))
    return redirect(url_for("views.rockets"))
@views.route('/delete_rocket_image', methods=['GET'])
def delete_rocket_image():
    database.delete_rocket_image(request.args.get("rocket_id"))
    return redirect(url_for("views.rockets"))

@views.route('/rockets/rocket_details_1', methods=['GET', 'POST'])
def rocket_details_1():
    rocket_d1 = database.get_rocket_d1()
    return render_template("rocket_details_1.html", rocket_details_1=rocket_d1)

# Ships
@views.route('/ships', methods=['GET', 'POST'])
def ships():
    ship_data = database.get_ships()
    ship_d1_data = database.get_ship_d1()
    ship_d2_data = database.get_ship_d2()

    inexistent_ship_d1 = []
    inexistent_ship_d2 = []
    inexistent_ship_d1_dict = []
    inexistent_ship_d2_dict = []

    present = False
    for ship in ship_data:
        for ship_d1 in ship_d1_data:
            if ship["ship_id"] == ship_d1["ship_id"]:
                present = True
                break
        if not present:
            inexistent_ship_d1 += [ship["ship_id"]]
            inexistent_ship_d1_dict += [{"ship_id": ship["ship_id"], "name": ship["name"]}]
        present = False

        for ship_d2 in ship_d2_data:
            if ship["ship_id"] == ship_d2["ship_id"]:
                present = True
                break
        if not present:
            inexistent_ship_d2 += [ship["ship_id"]]
            inexistent_ship_d2_dict += [{"ship_id": ship["ship_id"], "name": ship["name"]}]
        present = False  

    return render_template("ships.html", ships=ship_data,
        ship_d1s=ship_d1_data, ship_d2s=ship_d2_data, inexistent_d1=inexistent_ship_d1, inexistent_d2=inexistent_ship_d2, inexistent_d1_dict=inexistent_ship_d1_dict, inexistent_d2_dict=inexistent_ship_d2_dict,
        formM=forms.ShipForm(), formD1=forms.ShipD1Form(), formD2=forms.ShipD2Form())

@views.route("/add_ship", methods=["POST"])
def add_ship():
    database.add_ship(request)
    return redirect(url_for("views.ships"))
@views.route('/add_ship_detail_1', methods=['POST'])
def add_ship_detail_1():
    database.add_ship_d1(request)
    return redirect(url_for("views.ships"))
@views.route('/add_ship_detail_2', methods=['POST'])
def add_ship_detail_2():
    database.add_ship_d2(request)
    return redirect(url_for("views.ships"))

@views.route("/update_ship", methods=["POST"])
def update_ship():
    database.update_ship(request)
    return redirect(url_for("views.ships"))
@views.route('/update_ship_detail_1', methods=['POST'])
def update_ship_detail_1():
    database.update_ship_d1(request)
    return redirect(url_for("views.ships"))
@views.route('/update_ship_detail_2', methods=['POST'])
def update_ship_detail_2():
    database.update_ship_d2(request)
    return redirect(url_for("views.ships"))

@views.route('/delete_ship', methods=['GET'])
@login_required
def delete_ship():
    if current_user.is_admin:
        database.delete_ship(request.args.get("ship_id"))
    else:
        flash("Please do not poke around the exhibit.")
    return redirect(url_for("views.ships"))
@views.route('/delete_ship_detail_1', methods=['GET'])
def delete_ship_detail_1():
    database.delete_ship_d1(request.args.get("ship_id"))
    return redirect(url_for("views.ships"))
@views.route('/delete_ship_detail_2', methods=['GET'])
def delete_ship_detail_2():
    database.delete_ship_d2(request.args.get("ship_id"))
    return redirect(url_for("views.ships"))

@views.route('/ships/ship_details_1', methods=['GET', 'POST'])
def ship_details_1():
    ship_d1 = database.get_ship_d1()
    return render_template("ship_details_1.html", ship_details_1=ship_d1)


@views.route('/ships_filtered', methods=['GET', 'POST'])
def ships_filtered():
    filter_data = database.filter_ships(request)
    return render_template("ships.html", ships=filter_data, formM=forms.ShipForm())