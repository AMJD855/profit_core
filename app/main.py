from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import auth, calculator, trades, analytics

# إنشاء الجداول (في الإنتاج يفضل استخدام Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProfitCore API",
    description="Professional Financial API for Profit/Loss tracking",
    version="1.0.0"
)

# إعدادات CORS
origins = ["*"] # قم بتغيير هذا لرابط الفرونت إند عند النشر
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل الراوترات
app.include_router(auth.router)
app.include_router(calculator.router)
app.include_router(trades.router)
app.include_router(analytics.router)

# مراقبة الصحة (Health Check)
@app.get("/ping", tags=["Health"])
@app.head("/ping", tags=["Health"])
async def ping():
    return {"status": "ok", "service": "ProfitCore API"}

@app.get("/")
def root():
    return {"message": "Welcome to ProfitCore API. Go to /docs for Swagger UI"}

