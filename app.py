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
        cursor.execute("SELECT * FROM 'calorie track'")
        data = cursor.fetchall()
    return jsonify(data)


@app.route('/search-food/food/', methods=['POST'])
def search_Food():
    try:
        post_data = request.get_json()
        morning = post_data['morning']
        afternoon = post_data['afternoon']
        # evening = post_data['evening']

        with sqlite3.connect('calories') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM calorie_track WHERE foods=?", (morning,))
            data = cur.fetchall()

        with sqlite3.connect('calories') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM calorie_track WHERE foods=?", (afternoon,))
            data.append(cur.fetchall())
    except Exception as e:
        print('Something went wrong while feaching calorie track: ' + str(e))
    finally:
        con.close()
        return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True)
