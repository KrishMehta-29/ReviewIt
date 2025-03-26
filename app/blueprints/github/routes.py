from flask import request, jsonify
from . import github_bp  # Import the blueprint

from app import auth
from app.agentops_agent import getAICallFromDiff
import asyncio

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
        if payload.get('action') == 'review_requested':
            pull_request = payload['pull_request']

            reviewer = payload['requested_reviewer']
            if reviewer["login"] != "Review-It-Bot":
                return jsonify({'message': 'No need to add review for this reviewer'}), 200

            prNumber = pull_request['number']

            diff = auth.get_pull_request_diff("KrishMehta-29", "ReviewIt", prNumber)

            result = asyncio.run(askAiAndPushCommentsToGithub(diff, "KrishMehta-29", "ReviewIt", prNumber))
            return jsonify({"message": "Comments added to PR"}), 200
        return jsonify({'message': 'Event not handled'}), 200




async def askAiAndPushCommentsToGithub(diff, owner, repo, PrNumber):
    res = await getAICallFromDiff(diff)
    auth.push_comment_to_github(owner, repo, PrNumber, res)
    return 

