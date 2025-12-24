from fastapi import APIRouter, HTTPException
from app.schemas import schemas

# تعريف الراوتر هو السطر الذي يحل المشكلة
router = APIRouter(
    prefix="/calculator",
    tags=["Calculator"]
)

@router.post("/profit-loss", response_model=schemas.ProfitLossResponse)
def calculate_profit_loss(data: schemas.ProfitLossRequest):
    # حساب إجمالي قيمة الدخول والخروج
    total_entry = data.entry_price * data.quantity
    total_exit = data.exit_price * data.quantity
    
    # حساب الربح أو الخسارة الصافية
    raw_pnl = total_exit - total_entry
    net_pnl = raw_pnl - data.fee
    
    # حساب النسب المئوية
    percentage = (net_pnl / total_entry) * 100
    roi = (net_pnl / (total_entry + data.fee)) * 100
    
    status = "profit" if net_pnl > 0 else "loss" if net_pnl < 0 else "breakeven"
    
    return {
        "profit_or_loss": round(net_pnl, 2),
        "percentage": round(percentage, 2),
        "roi": round(roi, 2),
        "status": status
    }

