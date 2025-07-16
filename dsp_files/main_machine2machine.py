import os
import requests
import json
from dotenv import load_dotenv
import base64
import jwt

load_dotenv()

AUTH_URL        = os.environ["DSP_AUTH_URL"] 
HOSTNAME        = os.environ["DSP_BASE_URL"]
CLIENT_ID       = os.environ["CLIENT_ID_API_ACCESS"]
CLIENT_SECRET   = os.environ["CLIENT_SECRET_API_ACCESS"]

RESOURCE = "api/v1/dwc/consumption/relational/MHP_PLAYGROUND/GV_DD03L_002/GV_DD03L_002"
TOP = 20

def get_token_client_credentials():
    token_ep = f"{AUTH_URL}/oauth/token"
    payload = {
        "grant_type": "client_credentials"
    }
    # Standard: Basic Auth Header
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(
        token_ep,
        data=payload,
        headers=headers,
        timeout=30,
    )
    print(r.status_code, r.text)
    r.raise_for_status()
    return r.json()["access_token"]

def fetch_dsp(token: str, top: int):
    url = f"{HOSTNAME}{RESOURCE}"
    params = {
        "$top": top,
    }
    r = requests.get(
        url,
        params=params,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        },
        timeout=300,
    )
    print(r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def main():
    token = get_token_client_credentials()
    print(jwt.decode(token, options={"verify_signature": False}))
    data  = fetch_dsp(token, top=10)    
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
