from flask import request, jsonify
from . import github_bp  # Import the blueprint

from app import contract

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
        # if not auth.verifySignature(payloadBody, signature):
        #     return 'Invalid signature', 400

        # Parse the JSON payload
        payload = request.json

        # Handle the `review_requested` event
        handledWebhook = contract.handleWebhook(payload=payload)

        if handledWebhook: 
            return jsonify({"message": "Comments added to PR"}), 200
        return jsonify({'message': 'Event not handled'}), 200


