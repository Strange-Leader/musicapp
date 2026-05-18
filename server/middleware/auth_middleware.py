from fastapi import HTTPException, Header
import jwt

from dotenv import load_dotenv



load_dotenv()
import os
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def auth_middleware(x_auth_token=Header()):
    try:    
        if not x_auth_token:
            raise HTTPException (401, 'No auth token,acess denied')
        verified_token=jwt.decode(x_auth_token,JWT_SECRET,[ALGORITHM])

        if not verified_token:
            raise HTTPException(401,'Token verification failed')
        
        uid=verified_token.get('id')
        return {'uid':uid, 'token':x_auth_token}
    except jwt.PyJWTError:
        raise HTTPException(401,'Token is not valid')
pass