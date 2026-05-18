from fastapi import Depends ,HTTPException ,Header
import uuid
import bcrypt
from models.user import User
from pydantic_schemas.user_login import UserLogin
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from middleware.auth_middleware import auth_middleware
import jwt
from database import get_db
from dotenv import load_dotenv



load_dotenv()
import os
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
router=APIRouter()

@router.post('/signup',status_code=201)
def sign_user(user: UserCreate ,db:Session=Depends(get_db)):
    hashed_pw = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    user_db=db.query(User).filter(User.email == user.email).first()
    if user_db :
        raise HTTPException(400,'User with same username already exist')
       
    user_db=User(id=str(uuid.uuid4()),name=user.name , email=user.email, password =hashed_pw)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.post('/login')
def login_user(user:UserLogin, db: Session = Depends(get_db)):
    user_db=db.query(User).filter(User.email==user.email).first()
    if not user_db:
        raise HTTPException(400, 'User with this email does not exist')
    
    is_match =bcrypt.checkpw(user.password.encode(),user_db.password)
    if not is_match:
        raise HTTPException(404,"unauthorized")
    
    token = jwt.encode({'id':user_db.id},JWT_SECRET,ALGORITHM)
    return {'token':token , 'user':user_db}

@router.get('/')
def current_user_data(db: Session=Depends(get_db),user_dict=Depends(auth_middleware)):
    user=db.query(User).filter(User.id == user_dict['uid']).first()
    if not user:
        raise HTTPException(404,'User not found!')
    
    return user
pass