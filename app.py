import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS



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
@app.route('/enter-new/')
def reg():
    return render_template('index.html')

@app.route('/add-new/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            fname = request.form['fname']
            uname = request.form['uname']
            passw = request.form['passw']
            email = request.form['email']

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
            return msg


@app.route('/show-accounts/', methods=["GET"])
def show_accounts():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")
            records = cur.fetchall()
            for row in records:
                print(row)

            for i in row:
                print(i)

    except Exception as e:
        con.rollback()
        print("There was am error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)



@app.route('/delete-student/<int:accounts_id>/', methods=["GET"])
def delete_account(accounts_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM accounts WHERE id=" + str(accounts_id))
            con.commit()
            msg = "A account was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return render_template('delete-success.html', msg=msg)

if __name__=='__main__':
    app.run(debug=True)