from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: String

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Calculation Schemas ---
class ProfitLossRequest(BaseModel):
    capital: float
    entry_price: float
    exit_price: float
    quantity: float
    fee: float = 0.0

class ProfitLossResponse(BaseModel):
    profit_or_loss: float
    percentage: float
    roi: float
    status: str

# --- Trade Schemas ---
class TradeCreate(BaseModel):
    entry_price: float
    exit_price: float
    quantity: float
    profit_or_loss: float # يمكن حسابها أوتوماتيكياً أيضاً

class TradeResponse(TradeCreate):
    id: int
    created_at: datetime
    user_id: int
    class Config:
        from_attributes = True

# --- Analytics Schemas ---
class AnalyticsSummary(BaseModel):
    total_trades: int
    win_rate: float
    average_profit: float
    max_drawdown: float # Max loss
    smart_recommendation: str

