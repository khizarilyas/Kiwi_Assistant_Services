from flask import Flask, jsonify
import random
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "KhizarIlyas2008!",
    "database": "kiwi"
}

# Helper function to get DB connection
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route('/')
def home():
    return "Welcome to the REST API!"


# GET: Fetch all jokes
@app.route('/jokes', methods=['GET'])
def get_jokes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, category, setup, punchline FROM jokes"
    )
    jokes = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(jokes)


# GET: Fetch single joke by ID
@app.route('/jokes/<int:joke_id>', methods=['GET'])
def get_joke(joke_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, category, setup, punchline FROM jokes WHERE id = %s",
        (joke_id,)
    )
    joke = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(joke) if joke else ("Joke not found", 404)


# GET: Fetch random joke
@app.route('/jokes/random', methods=['GET'])
def get_random_joke():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, category, setup, punchline FROM jokes ORDER BY RAND() LIMIT 1"
    )
    joke = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(joke) if joke else ("Joke not found", 404)


if __name__ == '__main__':
    app.run(debug=True)


# # POST: Create a new user
# @app.route('/users', methods=['POST'])
# def create_user():
#     new_user = request.json
#     new_user["id"] = len(users) + 1
#     users.append(new_user)
#     return jsonify(new_user), 201
#
# # PUT: Update an existing user
# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user = next((u for u in users if u["id"] == user_id), None)
#     if user:
#         user.update(request.json)
#         return jsonify(user)
#     return ("User not found", 404)
#
# # DELETE: Delete a user
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     global users
#     users = [u for u in users if u["id"] != user_id]
#     return ("", 204)
