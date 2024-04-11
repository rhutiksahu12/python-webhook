from flask import Flask, request, jsonify
from pymongo import MongoClient
from extensions import client
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os


# Load Envs first
load_dotenv()

app = Flask(__name__)
CORS(app) 
db = client['webhook_data']
collection = db['events']

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.json
#     event_type = data['event_type']
#     payload = data['payload']
    
#     # Process webhook event and store in MongoDB
#     collection.insert_one({'event_type': event_type, 'payload': payload})
    
#     return 'Webhook received successfully', 200

# @app.route('/latest-events', methods=['GET'])
# def latest_events():
#     # Query MongoDB for latest events
#     events = list(collection.find().sort('_id', -1).limit(10))
#     formatted_events = format_events(events)
    
#     return jsonify(formatted_events), 200

# def format_events(events):
#     formatted_events = []
#     for event in events:
#         event_type = event['event_type']
#         payload = event['payload']
#         # Format events based on event_type
#         formatted_event = format_event(event_type, payload)
#         formatted_events.append(formatted_event)
#     return formatted_events

# def format_event(event_type, payload):
#     # Implement formatting logic based on event_type
#     # Example:
#     if event_type == 'push':
#         author = payload['head_commit']['author']['name']
#         to_branch = payload['ref'].split('/')[-1]
#         timestamp = payload['head_commit']['timestamp']
#         return f"{author} pushed to {to_branch} on {timestamp}"
#     elif event_type == 'pull_request':
#         author = payload['pull_request']['user']['login']
#         from_branch = payload['pull_request']['head']['ref']
#         to_branch = payload['pull_request']['base']['ref']
#         timestamp = payload['pull_request']['created_at']
#         return f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
#     elif event_type == 'merge':
#         author = payload['sender']['login']
#         from_branch = payload['pull_request']['head']['ref']
#         to_branch = payload['pull_request']['base']['ref']
#         timestamp = payload['pull_request']['merged_at']
#         return f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
#     else:
#         return ''


@app.route('/webhook', methods=['POST'])
def webhook():
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

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('timestamp', -1).limit(10))
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
