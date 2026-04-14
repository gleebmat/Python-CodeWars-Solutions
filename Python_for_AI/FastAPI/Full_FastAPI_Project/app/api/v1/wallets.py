from fastapi import FastAPI, HTTPException, APIRouter
from http import HTTPStatus
from pydantic import BaseModel, Field, field_validator
from app.api.v1.users import get_current_user
from app.models import User
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest
from app.dependency import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()


@router.get("/balance")
def get_balance(
    wallet_name: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallets_service.get_wallet(db, current_user, wallet_name)


@router.post("/wallets")
def create_wallet(
    wallet: CreateWalletRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallets_service.create_wallet(db, current_user, wallet)
