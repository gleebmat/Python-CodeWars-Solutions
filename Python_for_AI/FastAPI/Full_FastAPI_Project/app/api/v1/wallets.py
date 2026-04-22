from fastapi import FastAPI, HTTPException, APIRouter
from http import HTTPStatus
from pydantic import BaseModel, Field, field_validator
from app.api.v1.users import get_current_user
from app.models import User
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest, WalletResponse
from app.dependency import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()


@router.get("/balance")
async def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallets_service.get_total_balance(db, current_user)


@router.post(path="/wallets", response_model=WalletResponse)
def create_wallet(
    wallet: CreateWalletRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallets_service.create_wallet(db, current_user, wallet)


@router.get("/wallets", response_model=list[WalletResponse])
def get_all_wallets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return wallets_service.get_all_wallets(db, current_user)
