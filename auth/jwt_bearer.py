from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import jwt
import json


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token!")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token!")

    def verify_jwt(self, token: str):
        is_token_valid: bool = False

        try:
            payload = self.decode_token(token)
            if payload:
                if payload['scp'] == 'Middleware' and payload['azp'] == '09b59e37-7e0e-4c72-944a-12f78cf303bd':
                    is_token_valid = True
        except Exception:
            pass
        return is_token_valid

    def decode_token(self, token: str):
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
