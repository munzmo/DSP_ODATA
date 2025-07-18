import os, requests, json
from urllib.parse import urlencode, quote_plus
from dotenv import load_dotenv
import jwt

load_dotenv()

AUTH_URL      = os.environ["DSP_AUTH_URL"] 
HOSTNAME      = os.environ["DSP_BASE_URL"]
CLIENT_ID     = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

# URI from DSP
RESOURCE = "api/v1/dwc/consumption/relational/MHP_PLAYGROUND/GV_DD03L_002/GV_DD03L_002"
# Limit output
TOP = 20


def get_auth_code() -> str:
    params = {"response_type": "code", "client_id": CLIENT_ID}
    url = f"{AUTH_URL}/oauth/authorize?{urlencode(params, quote_via=quote_plus)}"
    print("Open URL and log in:\n", url, flush=True)
    return input("Paste the code= value: ").strip()


def exchange_code_for_token(code: str) -> str:
    token_ep = f"{AUTH_URL}/oauth/token"
    payload  = {"code": code, "grant_type": "authorization_code"}

    r = requests.post(
        token_ep,
        data=payload,
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]

# tabname: str, tabname='MARA'
def fetch_dsp(token: str, top: int = 20):
    url = f"{HOSTNAME}{RESOURCE}" 
    params = {
        #"$filter": f"TABNAME eq '{tabname}'",
        "$top":    top,
    }
    r = requests.get(
        url,
        params=params, 
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        timeout=300,
    )
    r.raise_for_status()
    return r.json()



def main():
    code  = get_auth_code()
    token = exchange_code_for_token(code)
    claims = jwt.decode(token, options={"verify_signature": False})
    print(claims)
    data  = fetch_dsp(token, top=10)

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
