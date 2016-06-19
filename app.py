#coding: utf-8
import psycopg2 as pg
from flask import Flask, jsonify
import ConfigParser

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
	script = """
		WITH s AS (SELECT * FROM odes where id = %s) SELECT row_to_json(s) FROM s;
	"""
	cu.execute(script, (id,))
	res = cu.fetchall()
	if res is None:
		raise ValueError
	else:
		return jsonify(res[0])

if __name__ == "__main__":
	app.run(port=9000, debug=True)
