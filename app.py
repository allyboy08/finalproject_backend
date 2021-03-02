import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, uname TEXT, passw TEXT, email TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()
app = Flask(__name__)
CORS(app)


@app.route('/')
# @app.route('/enter-new/')
# def reg():
#     return render_template('index.html')

@app.route('/add-new/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            uname = post_data['uname']
            passw = post_data['passw']
            email = post_data['email']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (fname, uname, passw, email) VALUES (?, ?, ?, ?)", (fname, uname, passw, email))
                con.commit()
                msg = fname + " Account succefully created."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

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

@app.route('/edit-account/<int:customer_id>/', methods=["PUT"])
def edit_account(customer_id):

    records= {
        'id': customer_id,
        'fname': request.json['fname'],
        'uname' : request.json['uname'],
        'passw' : request.json['passw'],
        'email' : request.json['email']
    }
    # Connecting to database
    con = sqlite3.connect('database.db')
    # Getting cursor
    cur = con.cursor()
    sql = ("UPDATE accounts SET fname = ?, uname = ?, passw = ?, email = ? WHERE id =?")
        # Editing data
    cur.execute(sql, (records['fname'],records['uname'], records['passw'], records['email'],records['id']))
        # Applying changes
    con.commit()
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


@app.route('/show-accounts/<int:customer_id>/', methods=["GET"])
def show_account(customer_id):
    records = {}
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts WHERE id=" + str(customer_id))
            records = cur.fetchone()
    except Exception as e:
        con.rollback()
        print("There was am error fetching results from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)




@app.route('/delete-account/', methods=["GET"])
def delete_account():
    records = {}
    msg = None
    try:
        post_data = request.get_json()

        passw = post_data['passw']
        with sqlite3.connect('database.db') as con:

            cur = con.cursor()
            sql = "DELETE * FROM accounts WHERE  passw = ?"
            cur.execute(sql, [passw])
            records = cur.fetchall()
            con.commit()
            msg = "A account was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(records)

if __name__=='__main__':
    app.run(debug=True)