import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def index():
	with psycopg.connect(
		host=os.getenv("DB_HOST"),
		port=os.getenv("DB_PORT", "5432"),
		dbname=os.getenv("DB_NAME"),
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASSWORD"),
	) as conn:
		with conn.cursor() as cur:
			cur.execute("SELECT version();")
			db_version = cur.fetchone()[0]

	return jsonify(
		status="ok",
		database=db_version
	)

app.run(host="0.0.0.0", port=8000)
