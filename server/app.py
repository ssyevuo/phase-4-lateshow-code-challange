#!/usr/bin/env python3

from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os
from sqlalchemy.orm import joinedload

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# retrieve episodes
@app.route('/episodes')
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict() for e in episodes]), 200

# retrieves episodes using id
@app.route('/episodes/<int:id>')
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return episode.to_dict(), 200

# delete an episode using id
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    db.session.delete(episode)
    db.session.commit()
    return '', 204

# retrieve guests
@app.route('/guests')
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests]), 200

# creates appearanes
@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    try:
        # Ensure all required fields are in the request data
        if 'rating' not in data or 'guest_id' not in data or 'episode_id' not in data:
            return jsonify({"errors": "Missing required fields (rating, guest_id, episode_id)"}), 400

        new_appearance = Appearance(
            rating=data['rating'],
            guest_id=data['guest_id'],
            episode_id=data['episode_id']
        )
        db.session.add(new_appearance)
        db.session.commit()
        
         # Load the related episode and guest before serializing
        new_appearance = Appearance.query.options(joinedload(Appearance.episode), joinedload(Appearance.guest)).get(new_appearance.id)

        return new_appearance.to_dict(), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
