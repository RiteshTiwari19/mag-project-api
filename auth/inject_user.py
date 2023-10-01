import json
import jwt
import requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from repositorties.UserRepository import UserRepository

oauth2_scheme = HTTPBearer()


def decode_token(token: str):
    jwks_response = requests.get('https://login.microsoftonline.com/common/discovery/keys')
    jwks_response.raise_for_status()
    jwks = json.loads(jwks_response.content)

    public_keys = {}
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    kid = jwt.get_unverified_header(token)['kid']
    key = public_keys[kid]

    payload = jwt.decode(token, key=key, algorithms=['RS256'], audience="a3cf94c4-ade1-4365-9f7c-a0d4d7fe28dc")

    return payload


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), user_repo: UserRepository = Depends()):
    payload = decode_token(token.credentials)
    user = user_repo.get_user_by_email(payload['preferred_username'])
    return user
