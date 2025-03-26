import hmac
import hashlib
import os

# GitHub Webhook Secret (set this when you create the app in GitHub)
GITHUB_SECRET = os.environ.get('GITHUB_SECRET')
# Function to verify webhook signature
def verifySignature(payloadBody, signature):
    # Create the expected signature
    computedSignature = 'sha256=' + hmac.new(
        bytes(GITHUB_SECRET, 'utf-8'),
        msg=payloadBody,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computedSignature, signature)