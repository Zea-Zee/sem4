from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
from my_parser import mvideo_prod_cards_parser
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
            # ("https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/",),
            # ("https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/",),
            # ("https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/",),
            ("https://www.mvideo.ru/playstation-4327/ps5-konsoli-8627",),
        ],
    )
    conn.commit()
    conn.close()


def clear_urls(db_path, urls=[]):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    if urls:
        # Удаляем только указанные URL-адреса
        cursor.execute("DELETE FROM suggestions WHERE url IN (?)", (tuple(urls),))
    else:
        # Удаляем все записи, если список URL-адресов пуст
        cursor.execute("DELETE FROM suggestions")
    conn.commit()
    conn.close()


def add_unique_urls(db_path, urls):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()

    clear_urls(db_path)

    unique_urls = set(urls)
    for url in unique_urls:
        cursor.execute("INSERT INTO suggestions (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()


def print_all_urls(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM suggestions")
    urls = cursor.fetchall()
    conn.close()

    print("All URLs in the database:")
    for url in urls:
        print(url[0])


clear_urls(db_path)
add_unique_urls(db_path, ['https://www.mvideo.ru/playstation-4327/ps5-konsoli-8627'])
print_all_urls(db_path)


@app.route("/check", methods=["GET"])
def check():
    # query = request.args.get("query")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM suggestions")
    suggestions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"suggestions": suggestions})


@app.route("/parse", methods=["GET"])
def parse_url():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        if 'mvideo.ru' in url:
            parsed_data = mvideo_prod_cards_parser(url)
            # print(parsed_data)
            if isinstance(parsed_data, list):
                return jsonify({
                    "products": parsed_data,
                    "status": "success"
                }), 200
            else:
                return jsonify({
                        "error": parsed_data,
                        "status": "Internal Server Error"
                    }), 500
        return jsonify({
            "error": "There is no suitable paerser for your url",
        }), 501
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


@app.errorhandler(404)
def page_not_found(error):
    return redirect("/parsepage")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
