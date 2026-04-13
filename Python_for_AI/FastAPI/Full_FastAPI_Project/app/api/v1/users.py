from fastapi import APIRouter
from app.schemas import UserRequest, UserResponse
from app.service import users as users_service
from sqlalchemy.orm import Session
from fastapi import Depends
from app.dependency import get_db

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(payload: UserRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db, payload.login)
