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
    with sqlite3.connect('calories.db') as con:
        con.row_factory = dict_factory
        cursor = con.cursor()
        cursor.execute('SELECT * FROM calorie track')
        data = cursor.fetchall()
    return jsonify(data)


@app.route('/search-food/food?/', methods=['POST'])
def search_Food():
    try:
        post_data = request.get_json()
        morning = post_data['morning']
        afternoon = post_data['afternoon']
        evening = post_data['evening']

        con = sqlite3.connect("calories.db")
        con.row_factory = dict_factory()
        cur = con.cursor()
        cur.execute("(SELECT * FROM calorie track where foods=?)", morning)
        data = cur.fetchall()
        print(data)
        return jsonify(data)
    except Exception as e:
        print(e)





if __name__ == '__main__':
    app.run(debug=True)
