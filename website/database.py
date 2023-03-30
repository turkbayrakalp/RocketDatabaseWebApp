import sqlite3
from flask import current_app

db_location = "spacexhibit-data.db"

# Capsules
def get_capsules():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM capsules"
            ).fetchall()

def add_capsule(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new capsule
        capsule_columns = cur.execute("PRAGMA table_info(capsules)").fetchall()
        
        new_capsule = []
        for column in capsule_columns:
            if column["name"] in request.form.keys():
                new_capsule += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO capsules VALUES ({",".join("?" * len(capsule_columns))})', new_capsule)
        con.commit()

def delete_capsule(capsule_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM capsules WHERE (capsule_id = ?)"
        cursor.execute(query, (capsule_id,))
        con.commit()

def update_capsule(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update capsule
        capsule_columns = cur.execute("PRAGMA table_info(capsules)").fetchall()
        capsule_columns_str = ",".join([column["name"] + "=?" for column in capsule_columns if column["name"] != "capsule_id"])

        capsule = []
        for column in capsule_columns:
            if column["name"] in request.form.keys():
                capsule += [request.form[column["name"]]]
        
        capsule_id = capsule[0]
        capsule = capsule[1:] + [capsule_id]

        cur.execute(f'UPDATE capsules SET {capsule_columns_str} WHERE capsule_id = ?', capsule)
        con.commit()

# Cores
def get_cores():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM cores"
            ).fetchall()

def add_core(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        core_columns = cur.execute("PRAGMA table_info(cores)").fetchall()

        new_core = [str(current_app.config["core_id"])]
        current_app.config["core_id"] += 1
        for column in core_columns:
            if column["name"] in request.form.keys():
                new_core += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO cores VALUES ({",".join("?" * len(core_columns))})', new_core)
        con.commit()
        
def delete_core(core_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        query = "DELETE FROM cores WHERE (core_id = ?)"
        cursor.execute(query, (core_id,))
        con.commit()

def update_core(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        core_columns = cur.execute("PRAGMA table_info(cores)").fetchall()
        core_columns_str = ",".join([column["name"] + "=?" for column in core_columns if column["name"] != "core_id"])

        core = []
        for column in core_columns:
            if column["name"] in request.form.keys():
                core += [request.form[column["name"]]]
        
        core_id = core[0]
        core = core[1:] + [core_id]

        cur.execute(f'UPDATE cores SET {core_columns_str} WHERE core_id = ?', core)
        con.commit()

def filter_core(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print("filter_core executed")
        query = "SELECT * FROM cores"
        params = []
        print(request.form.get('fserial'))
        if request.form.get('fserial'):
            if not params:
                query += " WHERE"
            user_serial = request.form['fserial']
            query += " serial LIKE ?"
            param_serial = "%" + user_serial + "%"
            params.append(param_serial)

        if request.form.get('fstatus'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_status = request.form['fstatus']
            query += " status LIKE ?"
            param_status = "%" + user_status + "%"
            params.append(param_status)

        if request.form.get('freuse_count') != "":
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_reuse_count = request.form['freuse_count']
            query += " reuse_count LIKE ?"
            param_reuse_count = "%" + user_reuse_count + "%"
            params.append(param_reuse_count)

        if request.form.get('fblock'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_block = request.form['fblock']
            query += " block LIKE ?"
            param_block = "%" + user_block + "%"
            params.append(param_block)

        if request.form.get('frtls_attempts'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_rtls_attempts = request.form['frtls_attempts']
            query += " rtls_attempts LIKE ?"
            param_rtls_attempts = "%" + user_rtls_attempts + "%"
            params.append(param_rtls_attempts)
        
        if request.form.get('frtls_landings'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_rtls_landings = request.form['frtls_landings']
            query += " rtls_landings LIKE ?"
            param_rtls_landings = "%" + user_rtls_landings + "%"
            params.append(param_rtls_landings)
        
        if request.form.get('fasds_attempts'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_asds_attempts = request.form['fasds_attempts']
            query += " asds_attempts LIKE ?"
            param_asds_attempts = "%" + user_asds_attempts + "%"
            params.append(param_asds_attempts)
        if request.form.get('fasds_landings'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_asds_landings = request.form['fasds_landings']
            query += " asds_landings LIKE ?"
            param_asds_landings = "%" + user_asds_landings + "%"
            params.append(param_asds_landings)

        print(query)
        print(tuple(params))
        filter = cur.execute(query, tuple(params)).fetchall()
        return filter

# Launches
def get_launches():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM launches LEFT JOIN launch_details on launches.launch_id = launch_details.launch_id"
            ).fetchall()

def get_launch_details():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            """SELECT * FROM launch_details 
            JOIN (SELECT launch_id, name FROM launches) AS launch_names
            ON launch_details.launch_id = launch_names.launch_id"""
            ).fetchall()

def add_launch(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new launch
        launch_columns = cur.execute("PRAGMA table_info(launches)").fetchall()
        
        new_launch = [str(current_app.config["launch_id"])]
        current_app.config["launch_id"] += 1
        for column in launch_columns:
            if column["name"] in request.form.keys():
                new_launch += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO launches VALUES ({",".join("?" * len(launch_columns))})', new_launch)
        con.commit()

def add_launch_details(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new launch_details
        launch_details_columns = cur.execute("PRAGMA table_info(launch_details)").fetchall()
        
        new_launch_details = []
        for column in launch_details_columns:
            if column["name"] in request.form.keys():
                new_launch_details += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO launch_details VALUES ({",".join("?" * len(launch_details_columns))})', new_launch_details)
        con.commit()

def delete_launch_details(launch_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM launch_details WHERE (launch_id = ?)"
        cursor.execute(query, (launch_id,))
        con.commit()

def filter_launches(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print("filter_launches executed")
        query = "SELECT * FROM launches"
        params = []
        print(request.form.get('fname'))
        if request.form.get('fname'):
            if not params:
                query += " WHERE"
            user_name = request.form['fname']
            query += " name LIKE ?"
            param_name = "%" + user_name + "%"
            params.append(param_name)

        if request.form.get('fdate'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_date = request.form['fdate']
            query += " date LIKE ?"
            param_date = "%" + user_date + "%"
            params.append(param_date)

        if request.form.get('ftime') != "":
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_time = request.form['ftime']
            query += " time LIKE ?"
            param_time = "%" + user_time + "%"
            params.append(param_time)

        if request.form.get('frocket_id'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_rocket_id = request.form['frocket_id']
            query += " rocket_id LIKE ?"
            param_rocket_id = "%" + user_rocket_id + "%"
            params.append(param_rocket_id)

        if request.form.get('flaunchpad_id'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_launchpad_id = request.form['flaunchpad_id']
            query += " launchpad_id LIKE ?"
            param_launchpad_id = "%" + user_launchpad_id + "%"
            params.append(param_launchpad_id)
        
        if request.form.get('fsuccess'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_success = request.form['fsuccess']
            query += " success LIKE ?"
            param_success = "%" + user_success + "%"
            params.append(param_success)
        
        if request.form.get('ffailure_reason'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_failure_reason = request.form['ffailure_reason']
            query += " failure_reason LIKE ?"
            param_failure_reason = "%" + user_failure_reason + "%"
            params.append(param_failure_reason)

        if request.form.get('fship'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_ship = request.form['faship']
            query += " ship LIKE ?"
            param_ship = "%" + user_ship + "%"
            params.append(param_ship)
        
        if request.form.get('fcapsules'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_capsules = request.form['fcapsules']
            query += " capsules LIKE ?"
            param_capsules = "%" + user_capsules + "%"
            params.append(param_capsules)

        print(query)
        print(tuple(params))
        filter = cur.execute(query, tuple(params)).fetchall()
        return filter

def delete_launch(launch_id):
        with sqlite3.connect(db_location) as con:
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")  # This allows for cascading to details
            query = "DELETE FROM launches WHERE (launch_id = ?)"
            cursor.execute(query, (launch_id,))
            con.commit()

def update_launch(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update launch
        launch_columns = cur.execute("PRAGMA table_info(launches)").fetchall()
        launch_columns_str = ",".join([column["name"] + "=?" for column in launch_columns if column["name"] != "launch_id"])

        launch = []
        for column in launch_columns:
            if column["name"] in request.form.keys():
                launch += [request.form[column["name"]]]
        
        launch_id = launch[0]
        launch = launch[1:] + [launch_id]

        cur.execute(f'UPDATE launches SET {launch_columns_str} WHERE launch_id = ?', launch)
        con.commit()

def update_launch_detail(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update launch_detail
        launch_detail_columns = cur.execute("PRAGMA table_info(launch_details)").fetchall()
        launch_detail_str = ",".join([column["name"] + "=?" for column in launch_detail_columns if column["name"] != "launch_id"])
        
        launch_detail = []
        for column in launch_detail_columns:
            if column["name"] in request.form.keys():
                launch_detail += [request.form[column["name"]]]

        launch_id = launch_detail[0]
        launch_detail = launch_detail[1:] + [launch_id]

        cur.execute(f'UPDATE launch_details SET {launch_detail_str} WHERE launch_id = ?', launch_detail)
        con.commit()

# Launchpads
def get_launchpads():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM launchpads ORDER BY name"
        )

# Payloads
def get_payloads():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM payloads ORDER BY name ASC"
            ).fetchall()

def filter_payloads(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print("filter_payloads executed")
        query = "SELECT * FROM payloads"
        params = []
        print(request.form.get('fname'))
        if request.form.get('fname'):
            if not params:
                query += " WHERE"
            user_name = request.form['fname']
            query += " name LIKE ?"
            param_name = "%" + user_name + "%"
            params.append(param_name)

        if request.form.get('ftype'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_type = request.form['ftype']
            query += " type LIKE ?"
            param_type = "%" + user_type + "%"
            params.append(param_type)

        if request.form.get('freused') != "":
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_reused = request.form['freused']
            query += " reused LIKE ?"
            param_reused = "%" + user_reused + "%"
            params.append(param_reused)

        if request.form.get('fmanufacturers'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_manufacturers = request.form['fmanufacturers']
            query += " manufacturers LIKE ?"
            param_manufacturers = "%" + user_manufacturers + "%"
            params.append(param_manufacturers)

        if request.form.get('forbit'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_orbit = request.form['forbit']
            query += " orbit LIKE ?"
            param_orbit = "%" + user_orbit + "%"
            params.append(param_orbit)
        
        if request.form.get('freference_system'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_reference_system = request.form['freference_system']
            query += " reference_system LIKE ?"
            param_reference_system = "%" + user_reference_system + "%"
            params.append(param_reference_system)
        
        if request.form.get('freference_system'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_regime = request.form['fregime']
            query += " regime LIKE ?"
            param_regime = "%" + user_regime + "%"
            params.append(param_regime)

        print(query)
        print(tuple(params))
        filter = cur.execute(query, tuple(params)).fetchall()
        return filter

def add_payload(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new payload
        payload_columns = cur.execute("PRAGMA table_info(payloads)").fetchall()

        new_payload = [str(current_app.config["payload_id"])]  # Get next ID
        current_app.config["payload_id"] += 1
        for column in payload_columns:
            if column["name"] in request.form.keys():
                new_payload += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO payloads VALUES ({",".join("?" * len(payload_columns))})', new_payload)
        con.commit()

def update_payload(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update payload
        payload_columns = cur.execute("PRAGMA table_info(payloads)").fetchall()
        payload_columns_str = ",".join([column["name"] + "=?" for column in payload_columns if column["name"] != "payload_id"])

        payload = []
        for column in payload_columns:
            if column["name"] in request.form.keys():
                payload += [request.form[column["name"]]]
        
        payload_id = payload[0]
        payload = payload[1:] + [payload_id]

        cur.execute(f'UPDATE payloads SET {payload_columns_str} WHERE payload_id = ?', payload)
        con.commit()

def delete_payload(payload_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        print("USER IS ADMIN, DELETE PAYLOAD")
        #cursor.execute("PRAGMA foreign_keys=ON")  # This allows for cascading to details
        query = "DELETE FROM payloads WHERE (payload_id = ?)"
        cursor.execute(query, (payload_id,))
        con.commit()
# Rockets
def get_rockets():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM rockets"
            ).fetchall()
def get_rocket_d1():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            """SELECT * FROM rocket_details_1 
            JOIN (SELECT rocket_id, name FROM rockets) AS rocket_names
            ON rocket_details_1.rocket_id = rocket_names.rocket_id"""
            ).fetchall()
def get_rocket_d2():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            """SELECT * FROM rocket_details_2 
            JOIN (SELECT rocket_id, name FROM rockets) AS rocket_names
            ON rocket_details_2.rocket_id = rocket_names.rocket_id"""
            ).fetchall()
def get_rocket_image():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        data = cur.execute(
            """SELECT * FROM rocket_images
            JOIN (SELECT rocket_id, name FROM rockets) AS rocket_names
            ON rocket_images.rocket_id = rocket_names.rocket_id"""
            ).fetchall()
        for row in data:
            try:
                with open("/static/rocket_images/" + row["rocket_id"] + ".png", "wb+") as image_file:
                    image_file.write(row["rocket_image"])
            except FileNotFoundError:
                with open("website/static/rocket_images/" + row["rocket_id"] + ".png", "wb+") as image_file:
                    image_file.write(row["rocket_image"])
        return data

def add_rocket(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new rocket
        rocket_columns = cur.execute("PRAGMA table_info(rockets)").fetchall()

        new_rocket = [str(current_app.config["rocket_id"])]  # Get next ID
        current_app.config["rocket_id"] += 1
        for column in rocket_columns:
            if column["name"] in request.form.keys():
                new_rocket += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO rockets VALUES ({",".join("?" * len(rocket_columns))})', new_rocket)
        con.commit()
def add_rocket_d1(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new rocket_d1
        rocket_d1_columns = cur.execute("PRAGMA table_info(rocket_details_1)").fetchall()
        
        new_rocket_d1 = []
        for column in rocket_d1_columns:
            if column["name"] in request.form.keys():
                new_rocket_d1 += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO rocket_details_1 VALUES ({",".join("?" * len(rocket_d1_columns))})', new_rocket_d1)
        con.commit()
def add_rocket_d2(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new rocket_d2
        rocket_d2_columns = cur.execute("PRAGMA table_info(rocket_details_2)").fetchall()
        
        new_rocket_d2 = []
        for column in rocket_d2_columns:
            if column["name"] in request.form.keys():
                new_rocket_d2 += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO rocket_details_2 VALUES ({",".join("?" * len(rocket_d2_columns))})', new_rocket_d2)
        con.commit()
def add_rocket_image(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new rocket_image
        
        new_rocket_image = [request.form["rocket_id"]]

        data = request.files["rocket_image"].read()
        print(data)

        new_rocket_image += [data]

        cur.execute(f'INSERT INTO rocket_images VALUES (?, ?)', new_rocket_image)
        con.commit()

def update_rocket(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update rocket
        rocket_columns = cur.execute("PRAGMA table_info(rockets)").fetchall()
        rocket_columns_str = ",".join([column["name"] + "=?" for column in rocket_columns if column["name"] != "rocket_id"])

        rocket = []
        for column in rocket_columns:
            if column["name"] in request.form.keys():
                rocket += [request.form[column["name"]]]
        
        rocket_id = rocket[0]
        rocket = rocket[1:] + [rocket_id]
        
        cur.execute(f'UPDATE rockets SET {rocket_columns_str} WHERE rocket_id = ?', rocket)
        con.commit()
def update_rocket_d1(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update rocket_d1
        rocket_d1_columns = cur.execute("PRAGMA table_info(rocket_details_1)").fetchall()
        rocket_d1_columns_str = ",".join([column["name"] + "=?" for column in rocket_d1_columns if column["name"] != "rocket_id"])
        
        rocket_d1 = []
        for column in rocket_d1_columns:
            if column["name"] in request.form.keys():
                rocket_d1 += [request.form[column["name"]]]

        rocket_id = rocket_d1[0]
        rocket_d1 = rocket_d1[1:] + [rocket_id]

        cur.execute(f'UPDATE rocket_details_1 SET {rocket_d1_columns_str} WHERE rocket_id = ?', rocket_d1)
        con.commit()
def update_rocket_d2(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update rocket_d2
        rocket_d2_columns = cur.execute("PRAGMA table_info(rocket_details_2)").fetchall()
        rocket_d2_columns_str = ",".join([column["name"] + "=?" for column in rocket_d2_columns if column["name"] != "rocket_id"])
        
        rocket_d2 = []
        for column in rocket_d2_columns:
            if column["name"] in request.form.keys():
                rocket_d2 += [request.form[column["name"]]]

        rocket_id = rocket_d2[0]
        rocket_d2 = rocket_d2[1:] + [rocket_id]

        cur.execute(f'UPDATE rocket_details_2 SET {rocket_d2_columns_str} WHERE rocket_id = ?', rocket_d2)
        con.commit()

def delete_rocket(rocket_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")  # This allows for cascading to details
        query = "DELETE FROM rockets WHERE (rocket_id = ?)"
        cursor.execute(query, (rocket_id,))
        con.commit()
def delete_rocket_d1(rocket_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM rocket_details_1 WHERE (rocket_id = ?)"
        cursor.execute(query, (rocket_id,))
        con.commit()
def delete_rocket_d2(rocket_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM rocket_details_2 WHERE (rocket_id = ?)"
        cursor.execute(query, (rocket_id,))
        con.commit()
def delete_rocket_image(rocket_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM rocket_images WHERE (rocket_id = ?)"
        cursor.execute(query, (rocket_id,))
        con.commit()

# Ships
def get_ships_only():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM ships"
            ).fetchall()

def get_ships(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if request.method == 'POST':
            query = "SELECT * FROM ships"
            params = []
            if request.form.get('name'):
                if not params:
                    query += " WHERE"
                user_name = request.form['name']
                query += " name LIKE ?"
                param_name = "%" + user_name + "%"
                params.append(param_name)

            if request.form.get('type'):
                if not params:
                    query += " WHERE"
                else:
                    query += " AND"
                user_type = request.form['type']
                query += " type LIKE ?"
                param_type = "%" + user_type + "%"
                params.append(param_type)

            if request.form.get('active'):
                user_active = request.form['active']
                if not params:
                    query += " WHERE"
                else:
                    query += " AND"
                query += " active LIKE ?"
                param_active = "%" + user_active + "%"
                print("paramactive: " + param_active)
                params.append(param_active)

            cur.execute(query, tuple(params))
            ships = cur.fetchall()
            cur.execute("SELECT * FROM ship_details_1 ORDER BY ship_id ASC")
            ship_details_1 = cur.fetchall()
        
        else:
            ships = cur.execute("SELECT * FROM ships ORDER BY ship_id ASC").fetchall()
            cur.execute("SELECT * FROM ship_details_1 ORDER BY ship_id ASC")
            ship_details_1 = cur.fetchall()

        return ships, ship_details_1

def get_ship_d1():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            """SELECT * FROM ship_details_1 
            JOIN (SELECT ship_id, name FROM ships) AS ship_names
            ON ship_details_1.ship_id = ship_names.ship_id"""
            ).fetchall()
            
def get_ship_d2():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            """SELECT * FROM ship_details_2 
            JOIN (SELECT ship_id, name FROM ships) AS ship_names
            ON ship_details_2.ship_id = ship_names.ship_id"""
            ).fetchall()

def add_ship(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new ship
        ship_columns = cur.execute("PRAGMA table_info(ships)").fetchall()

        new_ship = [str(current_app.config["ship_id"])]  # Get next ID
        current_app.config["ship_id"] += 1
        for column in ship_columns:
            if column["name"] in request.form.keys():
                new_ship += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO ships VALUES ({",".join("?" * len(ship_columns))})', new_ship)
        con.commit()

def add_ship_d1(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new ship_d1
        ship_d1_columns = cur.execute("PRAGMA table_info(ship_details_1)").fetchall()
        
        new_ship_d1 = []
        for column in ship_d1_columns:
            if column["name"] in request.form.keys():
                new_ship_d1 += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO ship_details_1 VALUES ({",".join("?" * len(ship_d1_columns))})', new_ship_d1)
        con.commit()

def add_ship_d2(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor() 

        # Add new ship_d2
        ship_d2_columns = cur.execute("PRAGMA table_info(ship_details_2)").fetchall()
        
        new_ship_d2 = []
        for column in ship_d2_columns:
            if column["name"] in request.form.keys():
                new_ship_d2 += [request.form[column["name"]]]

        cur.execute(f'INSERT INTO ship_details_2 VALUES ({",".join("?" * len(ship_d2_columns))})', new_ship_d2)
        con.commit()

def update_ship(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update ship
        ship_columns = cur.execute("PRAGMA table_info(ships)").fetchall()
        ship_columns_str = ",".join([column["name"] + "=?" for column in ship_columns if column["name"] != "ship_id"])

        ship = []
        for column in ship_columns:
            if column["name"] in request.form.keys():
                ship += [request.form[column["name"]]]
        
        ship_id = ship[0]
        ship = ship[1:] + [ship_id]
        
        cur.execute(f'UPDATE ships SET {ship_columns_str} WHERE ship_id = ?', ship)
        con.commit()

def update_ship_d1(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update ship_d1
        ship_d1_columns = cur.execute("PRAGMA table_info(ship_details_1)").fetchall()
        ship_d1_columns_str = ",".join([column["name"] + "=?" for column in ship_d1_columns if column["name"] != "ship_id"])
        
        
        ship_d1 = []
        for column in ship_d1_columns:
            if column["name"] in request.form.keys():
                ship_d1 += [request.form[column["name"]]]

        print("SHIP D1 COL STR: " + ship_d1_columns_str)
        ship_id = ship_d1[0]
        ship_d1 = ship_d1[1:] + [ship_id]

        cur.execute(f'UPDATE ship_details_1 SET {ship_d1_columns_str} WHERE ship_id = ?', ship_d1)
        con.commit()

def update_ship_d2(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Update ship_d2
        ship_d2_columns = cur.execute("PRAGMA table_info(ship_details_2)").fetchall()
        ship_d2_columns_str = ",".join([column["name"] + "=?" for column in ship_d2_columns if column["name"] != "ship_id"])
        
        ship_d2 = []
        for column in ship_d2_columns:
            if column["name"] in request.form.keys():
                ship_d2 += [request.form[column["name"]]]

        ship_id = ship_d2[0]
        ship_d2 = ship_d2[1:] + [ship_id]
        print(ship_d2)

        print("SHIP D2 COL STR: " + ship_d2_columns_str)
        cur.execute(f'UPDATE ship_details_2 SET {ship_d2_columns_str} WHERE ship_id = ?', ship_d2)
        con.commit()

def delete_ship(ship_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")  # This allows for cascading to details
        query = "DELETE FROM ships WHERE (ship_id = ?)"
        cursor.execute(query, (ship_id,))
        con.commit()
        
def delete_ship_d1(ship_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM ship_details_1 WHERE (ship_id = ?)"
        cursor.execute(query, (ship_id,))
        con.commit()
def delete_ship_d2(ship_id):
    with sqlite3.connect(db_location) as con:
        cursor = con.cursor()
        query = "DELETE FROM ship_details_2 WHERE (ship_id = ?)"
        cursor.execute(query, (ship_id,))
        con.commit()
def filter_ships(request):
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print("filter_ships executed")
        query = "SELECT * FROM ships"
        params = []
        print(request.form.get('fname'))
        if request.form.get('fname'):
            if not params:
                query += " WHERE"
            user_name = request.form['fname']
            query += " name LIKE ?"
            param_name = "%" + user_name + "%"
            params.append(param_name)

        if request.form.get('ftype'):
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_type = request.form['ftype']
            query += " type LIKE ?"
            param_type = "%" + user_type + "%"
            params.append(param_type)
        
        if request.form.get('factive') != "":
            if not params:
                query += " WHERE"
            else:
                query += " AND"
            user_active = request.form['factive']
            query += " active LIKE ?"
            param_active = "%" + user_active + "%"
            params.append(param_active)

        print(query)
        print(tuple(params))
        filter = cur.execute(query, tuple(params)).fetchall()
        return filter

def get_ships():
    with sqlite3.connect(db_location) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return cur.execute(
            "SELECT * FROM ships ORDER BY name ASC"
            ).fetchall()