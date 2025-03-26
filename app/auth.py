import hmac
import hashlib
import os
import jwt
import time
from cryptography.hazmat.primitives import serialization
import requests
import dotenv

dotenv.load_dotenv()

# GitHub Webhook Secret (set this when you create the app in GitHub)
GITHUB_SECRET = os.environ.get('GITHUB_SECRET')
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_SECRET_LOCATION = os.environ.get('GITHUB_SECRET_LOCATION')
GITHUB_API_URL = "https://api.github.com"



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

def generate_jwt():
    with open("reviewitbot.2025-03-25.private-key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": GITHUB_APP_ID,
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token():
    jwt_token = generate_jwt()
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get the installation ID of your app
    response = requests.get(f"{GITHUB_API_URL}/app/installations", headers=headers)
    response.raise_for_status()
    installations = response.json()
    
    if not installations:
        raise Exception("No installations found for this GitHub App.")

    installation_id = installations[0]["id"]  # Assuming first installation

    # Get an access token for the installation
    response = requests.post(
        f"{GITHUB_API_URL}/app/installations/{installation_id}/access_tokens",
        headers=headers,
    )
    response.raise_for_status()
    
    return response.json()["token"]

def list_open_pull_requests(owner, repo):
    token = get_installation_token()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls?state=open"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()


def get_pull_request_diff(owner, repo, pr_number):
    token = get_installation_token()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff",
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.text  # The response will be a raw diff

# diff = get_pull_request_diff("KrishMehta-29", "ReviewIt", 3)
def push_comment_to_github(owner, repo, pr_number, comment):
    token = get_installation_token()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    response = requests.post(url, headers=headers, json={"body": comment})
    response.raise_for_status()
    
    return response.json()

