from flask import Flask, request, jsonify

app = Flask(__name__)

favorite_things = [
    {"id": 1, "type": "movie", "title": "War Room"},
    {"id": 2, "type": "book", "title": "The Bible"},
    {"id": 3, "type": "game", "title": "PS"}
]

@app.route('/')
def index():
    return jsonify(message="Welcome to my favorite things API")

@app.route('/favorites', methods=['GET'])
def get_favorites():
    return jsonify(favorite_things), 200

@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorite(id):
    favorite = next((item for item in favorite_things if item["id"] == id), None)
    if favorite:
        return jsonify(favorite), 200
    return jsonify(error="Favorite not found"), 404

@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    print(f"Received data: {data}")

    if not data.get("title") or not data.get("type"):
        return jsonify(error="Title and type are required."), 400

    new_favorite = {
        "id": max([f["id"] for f in favorite_things]) + 1 if favorite_things else 1,
        "title": data["title"],
        "type": data["type"]
    }

    favorite_things.append(new_favorite)
    return jsonify(new_favorite), 201

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    global favorite_things
    favorite = next((item for item in favorite_things if item["id"] == id), None)
    if not favorite:
        return jsonify(error="Favorite not found"), 404

    favorite_things = [item for item in favorite_things if item["id"] != id]
    return jsonify(message="Favorite deleted"), 200

@app.route('/favorites/<int:id>', methods=['PUT'])
def update_favorite(id):
    data = request.get_json()
    favorite = next((item for item in favorite_things if item["id"] == id), None)

    if not favorite:
        return jsonify(error="Favorite not found"), 404

    favorite["title"] = data.get("title", favorite["title"])
    favorite["type"] = data.get("type", favorite["type"])

    return jsonify(favorite), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
