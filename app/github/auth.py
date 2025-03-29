import os
import jwt
import time
from cryptography.hazmat.primitives import serialization
import requests

GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_SECRET_LOCATION = os.environ.get('GITHUB_SECRET_LOCATION')
GITHUB_API_URL = "https://api.github.com"


def generateJwt():
    with open("reviewitbot.2025-03-25.private-key.pem", "rb") as keyFile:
        privateKey = serialization.load_pem_private_key(
            keyFile.read(),
            password=None
        )

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": GITHUB_APP_ID,
    }

    return jwt.encode(payload, privateKey, algorithm="RS256")


def getInstallationToken():
    jwtToken = generateJwt()
    
    headers = {
        "Authorization": f"Bearer {jwtToken}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get the installation ID of your app
    response = requests.get(f"{GITHUB_API_URL}/app/installations", headers=headers)
    response.raise_for_status()
    installations = response.json()
    
    if not installations:
        raise Exception("No installations found for this GitHub App.")

    installationId = installations[0]["id"]  # Assuming first installation

    # Get an access token for the installation
    response = requests.post(
        f"{GITHUB_API_URL}/app/installations/{installationId}/access_tokens",
        headers=headers,
    )
    response.raise_for_status()
    
    return response.json()["token"]

def getHeadersForRequest(getDiff=False):
    token = getInstallationToken()  # Get GitHub App token

    diffRequest = "application/vnd.github.v3.diff"
    jsonRequest = "application/vnd.github.v3+json"
    headers = {
        "Authorization": f"token {token}",
        "Accept": diffRequest if getDiff else jsonRequest,
    }

    return headers