from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import auth, calculator, trades, analytics
# استيراد الموديلات هنا ضروري لـ SQLite ليعرف الجداول التي سيقوم بإنشائها
from app.models import models 

# إنشاء الجداول تلقائياً (مثالي للمرحلة الأولى MVP باستخدام SQLite)
# سيقوم هذا الأمر بإنشاء ملف profitcore.db إذا لم يكن موجوداً
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProfitCore API",
    description="Professional Financial API for Profit/Loss tracking and Trade Management",
    version="1.0.0"
)

# إعدادات CORS للسماح بالوصول من أي مكان (أو تحديد روابط معينة لاحقاً)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل المسارات (Routers)
app.include_router(auth.router)
app.include_router(calculator.router)
app.include_router(trades.router)
app.include_router(analytics.router)

# نقطة فحص الحالة (Health Check) تدعم HEAD و GET لمراقبة UptimeRobot
@app.get("/ping", tags=["Health"])
@app.head("/ping", tags=["Health"])
async def ping():
    return {"status": "ok", "service": "ProfitCore API", "database": "SQLite"}

@app.get("/", tags=["General"])
def root():
    return {
        "message": "Welcome to ProfitCore API",
        "documentation": "/docs",
        "status": "Running"
    }

