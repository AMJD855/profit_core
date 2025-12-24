def calculate_pnl_logic(data):
    total_cost = (data.entry_price * data.quantity) + data.fee
    total_revenue = (data.exit_price * data.quantity)
    
    pnl = total_revenue - total_cost
    roi = (pnl / total_cost) * 100 if total_cost > 0 else 0
    percentage = (pnl / (data.capital if data.capital > 0 else total_cost)) * 100

    if pnl > 0:
        status = "profit"
    elif pnl < 0:
        status = "loss"
    else:
        status = "breakeven"
        
    return {
        "profit_or_loss": round(pnl, 2),
        "percentage": round(percentage, 2),
        "roi": round(roi, 2),
        "status": status
    }

