from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# --- User Schemas (Authentication) ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # تم التصحيح من String إلى str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True # لتمكين التحويل التلقائي من SQLAlchemy Models

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Profit & Loss Calculator Schemas ---

class ProfitLossRequest(BaseModel):
    capital: float = Field(..., gt=0, description="رأس المال الكلي")
    entry_price: float = Field(..., gt=0)
    exit_price: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    fee: float = Field(default=0.0, ge=0)

class ProfitLossResponse(BaseModel):
    profit_or_loss: float
    percentage: float
    roi: float
    status: str # profit | loss | breakeven

# --- Trade Tracker Schemas ---

class TradeCreate(BaseModel):
    entry_price: float
    exit_price: float
    quantity: float
    profit_or_loss: float

class TradeResponse(TradeCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Performance Analytics Schemas ---

class AnalyticsSummary(BaseModel):
    total_trades: int
    win_rate: float
    average_profit: float
    max_drawdown: float
    smart_recommendation: str

