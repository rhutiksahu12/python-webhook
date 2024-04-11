from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient
from ..extensions import client
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

db = client['webhook_data']
collection = db['events']


@webhook.route('/webhook', methods=['POST'])
def webhookData():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    if event_type in ['push', 'pull_request', 'merge']:
        event_data = {
            'action_type': event_type,
            'author': data['sender']['login'],
            'from_branch': data['pull_request']['head']['ref'] if event_type == 'pull_request' else data['before'],
            'to_branch': data['pull_request']['base']['ref'] if event_type == 'pull_request' else data['after'],
            'timestamp': datetime.utcnow()
        }
        collection.insert_one(event_data)
    return jsonify({'message': 'Received webhook event'}), 200

@webhook.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('timestamp', -1).limit(10))
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)