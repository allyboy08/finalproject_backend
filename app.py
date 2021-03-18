import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, uname TEXT, passw TEXT, email TEXT)')
    print("Table created successfully")
    # conn.execute(
    #     'CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, uname TEXT, passw TEXT)')
    # print("Table created successfully")
    conn.close()


init_sqlite_db()
app = Flask(__name__)
CORS(app)


@app.route('/')
def info():
    return "<p>/show-accounts/ is to show all registered users</p><p>/show-admin/ show the admin details</p>"
# @app.route('/enter-new/')
# def reg():
#     return render_template('index.html')

@app.route('/add-new/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            name = post_data['name']
            uname = post_data['uname']
            passw = post_data['passw']
            email = post_data['email']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (name, uname, passw, email) VALUES (?, ?, ?, ?)", (name, uname, passw, email))
                # cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','admin')",
                #             (uname, passw))
                con.commit()
                msg = name + " Account succefully created."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

def admin():
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()

            cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','1234')",
                        )
            con.commit()
            msg = " Admin succefully created."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        print(msg)
admin()
@app.route('/login-account/', methods=["GET"])
def login_account():
    records = {}
    if request.method == "POST":
        msg = None

        try:
            post_data = request.get_json()
            uname = post_data['uname']
            passw = post_data['passw']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM accounts WHERE uname = ? and passw = ?"
                cur.execute(sql, [uname, passw])
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            msg = "Error occurred while fetching data from db: " + str(e)
        finally:
            con.close()
            return jsonify(records)

@app.route('/login-admin/', methods=["GET"])
def login_admin():
    records = {}
    if request.method == "POST":
        msg = None

        try:
            post_data = request.get_json()
            uname = post_data['uname']
            passw = post_data['passw']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM admin WHERE uname = ? and passw = ?"
                cur.execute(sql, [uname, passw])
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            msg = "Error occurred while fetching data from db: " + str(e)
        finally:
            con.close()
            return jsonify(records)


@app.route('/edit-account/<int:customer_id>/', methods=["PUT"])
def edit_account(customer_id):

    post_data = request.get_json()

    records = {
        'id': customer_id,
        'name': post_data['name'],
        'uname': post_data['uname'],
        'passw': post_data['passw'],
        'email': post_data['email']
    }
    # Connecting to database
    con = sqlite3.connect('database.db')
    # Getting cursor
    cur = con.cursor()
    sql = ("UPDATE accounts SET name = ?, uname = ?, passw = ?, email = ? WHERE id =?")
        # Editing data
    cur.execute(sql, (records['name'],records['uname'], records['passw'], records['email'],records['id']))
        # Applying changes
    con.commit()
    return jsonify(records)




@app.route('/show-admin/', methods=["GET"])
def show_admin():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM admin")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was am error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)


@app.route('/show-accounts/', methods=["GET"])
def show_accounts():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was am error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)







@app.route('/delete-account/<int:customer_id>/', methods=["DELETE"])
def delete_account(customer_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:

            cur = con.cursor()
            cur.execute("DELETE FROM accounts WHERE  id = " + str(customer_id))

            con.commit()
            msg = "A account was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)

if __name__=='__main__':
    app.run(debug=True)