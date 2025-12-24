from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_user

router = APIRouter(prefix="/api/trades", tags=["Trades"])

@router.post("/", response_model=schemas.TradeResponse)
def create_trade(
    trade: schemas.TradeCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_trade = models.Trade(**trade.dict(), user_id=current_user.id)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

@router.get("/", response_model=List[schemas.TradeResponse])
def get_trades(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Trade).filter(models.Trade.user_id == current_user.id).all()

