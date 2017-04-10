# coding: utf-8
'''App service.'''

import os
import psycopg2 as pg
from flask import Flask, jsonify, render_template

MAXID = 305
host = os.getenv('POSTGRES_ADDR', 'localhost')
user = os.getenv('POSTGRES_USER', 'postgres')
password = os.getenv('POSTGRES_PASSWORD', '')

app = Flask(__name__)

db = pg.connect(database='odes', user=user,
                password=password, host=host, port='5432')
cu = db.cursor()


@app.route('/')
@app.route('/index.html')
def index():
    '''Hello world'''
    return render_template('index.html')


@app.route('/odes/<int:id>')
def get_ode_by_id(id):
    pre_id, next_id = id - 1, id + 1
    script = '''
        WITH s AS (SELECT * FROM odes where id=%s) SELECT row_to_json(s) FROM s;
    '''
    cu.execute(script, (id, ))
    res = cu.fetchone()
    script = '''
        WITH s AS (SELECT title FROM odes where id in (%s, %s)) SELECT array_to_json(array_agg(row_to_json(s))) FROM s;
    '''
    cu.execute(script, (pre_id, next_id))
    navi = cu.fetchone()
    if res is None or navi is None:
        raise ValueError
    else:
        res[0]['pre_title'] = navi[0][0].get('title') if id > 1 else None
        res[0]['next_title'] = navi[0][-1].get('title') if id < MAXID else None
        return jsonify(res[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
