from flask import Flask, jsonify, request
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
    return "Playlists API running"

# ----------------------------
# GET: All playlists
# ----------------------------
@app.route("/playlists", methods=["GET"])
def get_playlists():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM playlists;")
    playlists = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(playlists), 200

# ----------------------------
# POST: Create new playlist
# ----------------------------
@app.route("/playlists", methods=["POST"])
def create_playlist():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Playlist name required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO playlists (name) VALUES (%s);",
        (data["name"],)
    )
    conn.commit()

    playlist_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Playlist created",
        "playlist_id": playlist_id
    }), 201

# ----------------------------
# GET: Songs in a playlist
# ----------------------------
@app.route("/playlists/<int:playlist_id>", methods=["GET"])
def get_playlist_songs(playlist_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.id, s.name, s.artist, s.url
        FROM playlist_songs ps
        JOIN songs s ON ps.song_id = s.id
        WHERE ps.playlist_id = %s;
    """, (playlist_id,))

    songs = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "playlist_id": playlist_id,
        "songs": songs
    }), 200

# ----------------------------
# POST: Add song to playlist
# ----------------------------
@app.route("/playlists/<int:playlist_id>/add", methods=["POST"])
def add_song_to_playlist(playlist_id):
    data = request.get_json()

    if not data or "song_id" not in data:
        return jsonify({"error": "song_id required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT IGNORE INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s);",
        (playlist_id, data["song_id"])
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Song added to playlist",
        "playlist_id": playlist_id,
        "song_id": data["song_id"]
    }), 200

# ----------------------------
# DELETE: Remove song from playlist
# ----------------------------
@app.route("/playlists/<int:playlist_id>/remove/<int:song_id>", methods=["DELETE"])
def remove_song_from_playlist(playlist_id, song_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM playlist_songs WHERE playlist_id=%s AND song_id=%s;",
        (playlist_id, song_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Song removed from playlist",
        "playlist_id": playlist_id,
        "song_id": song_id
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5003)
