import hmac
import hashlib
import os
import dotenv

dotenv.load_dotenv()

# GitHub Webhook Secret (set this when you create the app in GitHub)
GITHUB_SECRET = os.environ.get('GITHUB_SECRET')

# Function to verify webhook signature
def verifySignature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise Exception("Misisng")
    hash_object = hmac.new(GITHUB_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    print(expected_signature)
    print(signature_header)
    if not hmac.compare_digest(expected_signature, signature_header):
        raise Exception("Mismatch")
    
    return True 
