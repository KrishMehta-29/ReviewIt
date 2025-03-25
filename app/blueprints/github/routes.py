from flask import request, jsonify
from . import github_bp  # Import the blueprint

@github_bp.route('/')
def index():
    return jsonify("Hello World")


from flask import Flask, request, jsonify
import hmac
import hashlib

import os

# GitHub Webhook Secret (set this when you create the app in GitHub)
GITHUB_SECRET = os.environ.get('GITHUB_SECRET')

# Function to verify webhook signature
def verify_signature(payload_body, signature):
    # Create the expected signature
    computed_signature = 'sha256=' + hmac.new(
        bytes(GITHUB_SECRET, 'utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

@github_bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Get the GitHub signature header
        signature = request.headers.get('X-Hub-Signature-256')
        payload_body = request.get_data()

        # Verify the payload signature
        if not verify_signature(payload_body, signature):
            return 'Invalid signature', 400

        # Parse the JSON payload
        payload = request.json

        print(payload)

        # Handle the `review_requested` event
        if payload.get('action') == 'review_requested':
            pull_request = payload['pull_request']
            reviewer = payload['review_request']['reviewer']

            # Example: Do something with the pull request data
            print(f"Review requested on PR #{pull_request['number']} by {reviewer['login']}")

            # Respond with a success message
            return jsonify({'message': 'Review requested event processed successfully'}), 200

        return jsonify({'message': 'Event not handled'}), 200

