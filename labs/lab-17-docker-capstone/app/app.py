import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
	return psycopg.connect(
		host=os.getenv("DB_HOST", "db"),
		port=os.getenv("DB_PORT", "5432"),
		dbname=os.getenv("DB_NAME"),
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASSWORD"),
	)

def ensure_table(conn):
	with conn.cursor() as cur:
		cur.execute("""
			CREATE TABLE IF NOT EXISTS visit_counter (
				id INTEGER PRIMARY KEY,
				visits INTEGER NOT NULL
			);
		""")

		cur.execute("""
			INSERT INTO visit_counter (id, visits)
			VALUES (1, 0)
			ON CONFLICT (id) DO NOTHING;
		""")

	conn.commit()


@app.get("/")
def index():
	return jsonify(
		app="docker-capstone",
		status="ok"
	)

@app.get("/health")
def health():
	return jsonify(status="healthy")

@app.get("/visits")
def get_visits():
	with get_connection() as conn:
		ensure_table(conn)

		with conn.cursor() as cur:
			cur.execute(
				"SELECT visits FROM visit_counter WHERE id = 1;"
			)
			visits = cur.fetchone()[0]

	return jsonify(visits=visits)

@app.post("/visits")
def add_visit():
	with get_connection() as conn:
		ensure_table(conn)

		with conn.cursor() as cur:
			cur.execute("""
				UPDATE visit_counter
				SET visits = visits + 1
				WHERE id = 1
				RETURNING visits;
			""")

			visits = cur.fetchone()[0]

		conn.commit()

	return jsonify(visits=visits)

if __name__ == "__main__":
	app.run(
		host="0.0.0.0",
		port=8000
	)
