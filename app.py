from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favorites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)


    def to_dict(self):
        return {"id": self.id, "title": self.title, "type": self.type}

@app.route('/')
def index():
    return jsonify(message="Welcome to my favorite things API")

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([fav.to_dict() for fav in favorites])

@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite:
        return jsonify(favorite.to_dict())
    return jsonify(error="Favorite not found"), 404

@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()

    if not data.get("title") or not data.get("type"):
        return jsonify(error="Title and type are required."), 400

    new_favorite = Favorite(title=data["title"], type=data["type"])
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.to_dict()), 201

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if not favorite:
        return jsonify(error="Favorite not found"), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify(message="Favorite deleted"), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
