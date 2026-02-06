from app.main import FastAPI

# 라우터 연결(엔드포인트 묶음)
from app.api.routes import products, ai  

# FastAPI 앱 생성(서버 진입점)
APP = FastAPI(title="AI-NutriCurator (Backend Skeleton)", version="0.0.1")

# /products 아래로 products 라우터를 붙임
APP.include_router(products.router, prefix="/products", tags=["products"])

# /ai 아래로 ai 라우터를 붙임(현재는 popu만)
APP.include_router(ai.router, prefix="/ai", tags=["ai"])


# 서버 살아있는지 체크용
@APP.get("/healthz")
def healthz():
    return {"ok": True}


# "가상 이커머스 사이트 들어가기" 버튼용
@APP.get("/entry")
def entry():
    return {
        "message": "Entry OK (backend skeleton only)",
        "next_actions": [
            "GET /products",
            "POST /ai/popu",
        ],
    }
