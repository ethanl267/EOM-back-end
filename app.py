import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    x = {}
    for idx, col in enumerate(cursor.description):
        x[col[0]] = row[idx]
    return x


@app.route('/food/', methods=['GET'])
def show_data():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cursor = con.cursor()
            cursor.execute('SELECT * FROM calorie')
            data = cursor.fetchall()
        return jsonify(data)
    except:
        pass


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin_code = request.form['pin-code']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO student (name, address, city, pin_code) VALUES (?, ?, ?, ?)",
                            (name, address, city, pin_code))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)
