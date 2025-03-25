from flask import request, jsonify
from . import github_bp  # Import the blueprint

from app import auth

@github_bp.route('/')
def index():
    return jsonify("Hello World")

@github_bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Get the GitHub signature header
        signature = request.headers.get('X-Hub-Signature-256')
        payloadBody = request.get_data()

        # Verify the payload signature
        if not auth.verifySignature(payloadBody, signature):
            return 'Invalid signature', 400

        # Parse the JSON payload
        payload = request.json

        # Handle the `review_requested` event
        if payload.get('action') == 'review_requested':
            pull_request = payload['pull_request']

            reviewer = payload['requested_reviewer']
            print(reviewer)

            # TODO: Here we got to add more info. Would ideally organize it a little better tbh but yeah for now. 


            # Respond with a success message
            return jsonify({'message': 'Review requested event processed successfully'}), 200

        return jsonify({'message': 'Event not handled'}), 200

