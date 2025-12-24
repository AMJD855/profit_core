from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary", response_model=schemas.AnalyticsSummary)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    trades = db.query(models.Trade).filter(models.Trade.user_id == current_user.id).all()
    
    if not trades:
        return {
            "total_trades": 0, "win_rate": 0, "average_profit": 0,
            "max_drawdown": 0, "smart_recommendation": "Start trading to see analytics."
        }

    total_trades = len(trades)
    wins = sum(1 for t in trades if t.profit_or_loss > 0)
    win_rate = (wins / total_trades) * 100
    avg_profit = sum(t.profit_or_loss for t in trades) / total_trades
    max_loss = min([t.profit_or_loss for t in trades] + [0])

    # توصية ذكية بسيطة
    if win_rate < 40:
        rec = "Review your strategy; win rate is low."
    elif max_loss < -1000: # مثال
        rec = "Manage your risk better, huge drawdowns detected."
    else:
        rec = "Good performance, keep consistent."

    return {
        "total_trades": total_trades,
        "win_rate": round(win_rate, 2),
        "average_profit": round(avg_profit, 2),
        "max_drawdown": max_loss,
        "smart_recommendation": rec
    }

