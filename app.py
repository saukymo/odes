#coding: utf-8
import psycopg2 as pg
from flask import Flask, jsonify
import ConfigParser


MAXID = 305

cf = ConfigParser.ConfigParser()
cf.read('dev.conf')

host = cf.get("database", "host")
user = cf.get("database", "user")
password = cf.get("database", "password")

app = Flask(__name__)

db = pg.connect(database="odes", user=user, password=password, host=host, port="5432") 
cu = db.cursor()

@app.route("/")
def index():
	return "Hello World!"

@app.route("/odes-api/<int:id>")
def get_ode_by_id(id):
	min_id, max_id = id - 1, id + 1
	if (id == 1):
		min_id = MAXID
	if (id == MAXID):
		max_id = 1
	script = """
		WITH s AS (SELECT * FROM odes where id in (%s, %s, %s)) SELECT array_to_json(array_agg(row_to_json(s))) FROM s;
	"""
	cu.execute(script, (min_id, id, max_id))
	res = cu.fetchone()
	if (id == 1):
		res[0][0], res[0][1], res[0][2] = res[0][2], res[0][0], res[0][1]
	if (id == MAXID):
		res[0][0], res[0][1], res[0][2] = res[0][1], res[0][2], res[0][0]
	if res is None:
		raise ValueError
	else:
		return jsonify(res[0])

if __name__ == "__main__":
	app.run(port=9000, debug=True)
