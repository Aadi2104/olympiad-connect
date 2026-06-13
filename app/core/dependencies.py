from fastapi import Depends,Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm.session import Session
from app.services.user_services import UserServices
from app.core.security import decode_access_token
from app.core.errors import TokenNotFound, InvalidToken , NotAuthorized
from app.models.user_model import User, UserRole
from app.db.session import get_db
from typing import Any,List
import jwt


user_services=UserServices()

class TokenBearer(HTTPBearer):

    async def __call__(self, request:Request) -> dict[str,Any]:
        
    
        cred = await super().__call__(request) 
        
     

        token = cred.credentials

        try:
            token_data = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            raise InvalidToken("Access token has expired")
        except jwt.InvalidTokenError:
            raise InvalidToken("Invalid access token")
 

        return token_data


def get_current_user(token_data:dict[str,Any] = Depends(TokenBearer()),session:Session=Depends(get_db)) ->User:
    user_id=token_data.get("user_id")
    user = user_services.get_user(user_id,session)
    return user


class RoleChecker():
    def __init__(self,allowed_roles:List[UserRole]):
        self.allowed_roles = allowed_roles
        
    def __call__(self, user:User = Depends(get_current_user)) -> None:
        user_role = user.role
        if user_role not in self.allowed_roles:
            raise NotAuthorized()
        
        
    