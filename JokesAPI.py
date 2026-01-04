from flask import Flask, jsonify  # Flask app and JSON response helper
import random  # Used to select a random joke

app = Flask(__name__)  # Create Flask application instance

# Sample in-memory "database"
jokes = [
    {"id": 1, "setup": "Why don’t scientists trust atoms?", "punchline": "Because they make up everything."},
    {"id": 2, "setup": "Why did the scarecrow get promoted?", "punchline": "Because he was outstanding in his field."},
    {"id": 3, "setup": "Why did the golfer bring two pairs of pants?", "punchline": "n case he got a hole in one."},
    {"id": 4, "setup": "Why don’t skeletons fight each other?", "punchline": "They don’t have the guts."}
]

@app.route('/')  # Root endpoint
def home():
    return "Welcome to the REST API!"  # Simple status response

# GET: Fetch all jokes
@app.route('/jokes', methods=['GET'])
def get_jokes():
    return jsonify(jokes)  # Return all jokes as JSON

# GET: Fetch single jokes by ID randomly
@app.route('/jokes/<int:joke_id>', methods=['GET'])
def get_joke(joke_id):
    # Find a joke matching the provided ID
    joke = next((j for j in jokes if j["id"] == joke_id), None)
    return jsonify(joke) if joke else ("Joke not found", 404)

# GET: Fetch single jokes by ID randomly
@app.route('/jokes/random', methods=['GET'])
def get_random_joke():
    # Select a random joke ID from the list
    random_id = random.choice(jokes)["id"]

    # Find and return the joke with that ID
    joke = next((j for j in jokes if j["id"] == random_id), None)
    return jsonify(joke) if joke else ("Joke not found", 404)

if __name__ == '__main__':
    app.run(debug=True)  # Start Flask development server




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
