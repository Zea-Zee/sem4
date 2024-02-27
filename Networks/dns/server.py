from flask import Flask, request, jsonify, render_template
import sqlite3
from parser import dns_prod_cards_parser
import os


app = Flask(__name__)


db_path = os.path.join(os.path.dirname(__file__), "database.db")


if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS suggestions (id INTEGER PRIMARY KEY, url TEXT)"""
    )
    cursor.executemany(
        "INSERT INTO suggestions (url) VALUES (?)",
        [
            ("https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/",),
            ("https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/",),
            ("https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/",),
        ],
    )
    conn.commit()
    conn.close()


@app.route("/check", methods=["GET"])
def check():
    query = request.args.get("query")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM suggestions WHERE url LIKE ?", ("%" + query + "%",))
    suggestions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"suggestions": suggestions})


@app.route("/parse", methods=["GET"])
def parse_url():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        parsed_data = dns_prod_cards_parser(url)
        return jsonify(parsed_data)
    except Exception as e:
        return jsonify({"error": f"in parse_url function: {e}"}), 500


@app.route("/parsepage", methods=["GET"])
def parse_page():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM suggestions")
    suggestions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template("parse_page.html", suggestions=suggestions)


if __name__ == "__main__":
    app.run(port=8000)
