from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "KhizarIlyas2008!",
    "database": "kiwi"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return "Welcome to the REST API!"

# GET: Fetch single song by name (FULLTEXT search)
@app.route("/songs/<path:song_name>", methods=["GET"])
def get_song(song_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    song_name_clean = song_name.strip().lower()
    song_name_compact = song_name_clean.replace(" ", "")

    cursor.execute(
        "SELECT id, name, artist, url FROM kiwi.Songs WHERE name_compact = %s LIMIT 1;",
        (song_name_compact,)
    )
    song = cursor.fetchone()

    cursor.close()
    connection.close()

    if song is None:
        return jsonify({"error": "Song not found", "searched": song_name_clean}), 404

    return jsonify(song), 200

# GET: Fetch single song randomly
@app.route("/songs/random", methods=["GET"])
def get_random_song():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, artist, url FROM kiwi.Songs ORDER BY RAND() LIMIT 1;"
    )
    song = cursor.fetchone()

    cursor.close()
    connection.close()

    if song is None:
        return jsonify({"error": "Song not found"}), 404

    return jsonify(song), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
