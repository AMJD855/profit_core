from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)

# 1. إضافة صفقة جديدة (POST)
@router.post("/", response_model=schemas.TradeResponse)
def create_trade(
    trade: schemas.TradeCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    new_trade = models.Trade(
        **trade.model_dump(), # تحويل بيانات Pydantic إلى قاموس
        user_id=current_user.id # ربط الصفقة بالمستخدم الحالي
    )
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

# 2. جلب جميع صفقات المستخدم الحالي (GET)
@router.get("/", response_model=List[schemas.TradeResponse])
def get_user_trades(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    trades = db.query(models.Trade).filter(models.Trade.user_id == current_user.id).all()
    return trades

