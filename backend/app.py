# -*- coding: utf-8 -*-
"""
AI-NutriCurator Backend API
FastAPI 기반 알러지 분석 및 제품 추천 서버
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import json

app = FastAPI(title="AI-NutriCurator API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== 데이터 모듈 ==============

products = {
    "0": {
        "product_id": "201905000000",
        "name": "설화눈꽃팝김부각스낵",
        "category": "과자",
        "ingredients": ["찹쌀", "김", "참깨", "옥수수기름(옥배유)", "양파", "무", "대파", "천일염", "마늘", "새우", "멸치", "다시마", "건표고버섯", "둥굴레", "감초", "정제수"],
        "allergy": "없음",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=설화눈꽃팝김부각스낵"
    },
    "1": {
        "product_id": "201804000000",
        "name": "설화눈꽃팝김부각스낵 아몬드맛",
        "category": "과자",
        "ingredients": ["찹쌀", "김", "참깨", "옥수수기름(옥배유)", "아몬드", "양파", "무", "천일염", "대파", "마늘", "새우", "멸치", "다시마", "건표고버섯", "둥굴레", "감초", "정제수"],
        "allergy": "아몬드",
        "trace": "",
        "image": "https://via.placeholder.com/300x200?text=아몬드맛"
    },
    "2": {
        "product_id": "201804000000",
        "name": "고들빼기김치",
        "category": "김치류",
        "ingredients": ["고들빼기", "멸치액", "염장새우", "L-글루타민산나트륨", "양파", "다시마육수", "혼합간장", "고춧가루", "마늘", "생강", "갈색설탕", "참깨", "물엿", "매실청", "배즙", "찹쌀풀", "당근", "파", "파"],
        "allergy": "새우,대두,밀",
        "trace": "밀, 땅콩, 복숭아, 토마토, 호두, 아황산류 혼입 가능",
        "image": "https://via.placeholder.com/300x200?text=고들빼기김치"
    },
    "3": {
        "product_id": "19950400000000",
        "name": "해태 허니버터칩",
        "category": "과자",
        "ingredients": ["감자(미국산)", "혼합식용유[팜올레인유(말레이시아산)59.98%", "해바라기유(수입산)40%", "토코페롤(혼합형)]", "복합조미식품[허니버터맛시즈닝(결정과당", "백설탕", "정제소금", "탈지분유(우유)", "버터혼합분말65(대두)", "이스트익스트랙트파우다YE3(효모추출물)", "천연향신료(파슬리후레이크)", "아카시아꿀분말(아카시아꿀(국내산))", "고메버터(프랑스산))(밀)]]"],
        "allergy": "우유,대두,밀",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=허니버터칩"
    },
    "4": {
        "product_id": "20140500000000",
        "name": "헬로버블 라이스퍼프 양파맛",
        "category": "과자",
        "ingredients": ["현미73.55%(유기농,국산)", "어니언시즈닝12.24%{정백당", "결정포도당", "말토덱스트린", "리치버터분말", "양파분7.24%(중국산)", "합성향료(구운양파향)", "L-글루탐산나트륨(향미증진제)}", "백미7.36%(유기농,국산)", "유기이소말토쌀올리고당", "정제수", "옥수수과립", "비타민E혼합제제분말(변성전분)", "유기농설탕"],
        "allergy": "알수없음",
        "trace": "본 제품은 돼지고기, 땅콩, 복숭아, 아황산류, 호두를 사용한 제품과 같은 제조시설에서 제조하고 있습니다.",
        "image": "https://via.placeholder.com/300x200?text=라이스퍼프"
    },
    "5": {
        "product_id": "201105000000",
        "name": "두마리목장 콜비치즈",
        "category": "유제품",
        "ingredients": ["원유(국산)99.9%", "우유응고효소", "유산균", "식염", "안나토색소(천연색소)"],
        "allergy": "우유함유",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=콜비치즈"
    },
    "6": {
        "product_id": "2011050000000",
        "name": "양반 바삭 튀김가루",
        "category": "가루류",
        "ingredients": ["밀가루(밀/미국산)", "변성전분", "베이킹파우더(팽창제,산도조절제,전분)", "정제소금(국내산)", "양파분말0.5%(양파100%/중국산)", "옥수수가루", "백후추분말"],
        "allergy": "밀",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=튀김가루"
    },
    "7": {
        "product_id": "2011040000000",
        "name": "돈목살훈제바베큐스테이크",
        "category": "육류",
        "ingredients": ["돼지고기(목살,외국산-국가명www.yellowfarm.co.kr/별도표기)96.68%", "스모크시즈닝-1{복합스파이스AS-1[분리대두단백(중국산),정제소금(국내산)]}", "토마토케찹", "아질산나트륨(발색제)", "파슬리후레이크"],
        "allergy": "돼지고기,밀,우유,대두,쇠고기,토마토 함유",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=훈제스테이크"
    },
    "8": {
        "product_id": "2011040000000",
        "name": "태양초 고추장 골드",
        "category": "양념류",
        "ingredients": ["고춧가루2.84%(국산)", "물엿", "소맥분(밀:미국산,호주산)", "혼합양념(중국산태양초고춧가루6.49%,정제소금,마늘,양파/중국산)", "밀쌀", "분말혼합양념(고춧가루0.99%,밀쌀가루,정제소금,포도당,찹쌀가루,마늘분/중국산)", "정제소금", "정백당", "주정", "종국"],
        "allergy": "밀",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=고추장"
    },
    "9": {
        "product_id": "2011040000000",
        "name": "환타지 믹스너트",
        "category": "견과류",
        "ingredients": ["커피땅콩[(중국)땅콩52%,설탕,커피1.4%,고구마전분]10%", "화이트볼[(중국)설탕55.71%,땅콩42.86%,옥수수전분]10%", "찹쌀땅콩[(중국)/땅콩39.91%,밀가루,설탕,찹쌀가루12.87%,물엿,중탄산암모늄(팽창제),젤라틴(돼지),L-글루타민산나트륨(향미증진제),말토덱스트린]15%", "튀김땅콩[(중국)땅콩95.8%,팜유3.2%,소금]15%", "로스티드피터츠[(베트남)땅콩50%,밀가루,백설탕,코코넛유,코코넛주스]15%", "바나나칩[(필리핀)바나나65.5%,코코넛오일,설탕,천연바나나향]15%", "볶음아몬드[(미국)아몬드100%]10%", "꿀땅콩[(중국)땅콩53.60%,설탕,밀가루,꿀,찰옥수수변성전분(아세틸아디핀산이전분),커피]10%"],
        "allergy": "땅콩,밀,돼지고기,아몬드",
        "trace": "null",
        "image": "https://via.placeholder.com/300x200?text=믹스너트"
    }
}

final_profiles = {
    "0": {
        "user_id": "0",
        "name": "당뇨 + 우유/땅콩 알러지 환자",
        "restricted_ingredients": ["우유", "땅콩"],
        "sugar": 5.0,
        "description": "당뇨병 환자이며 우유와 땅콩에 알러지가 있습니다."
    },
    "1": {
        "user_id": "1",
        "name": "고혈압 + 새우 알러지 환자",
        "restricted_ingredients": ["새우"],
        "sodium": 2300.0,
        "potassium_min": 3500.0,
        "fat_ratio": 0.25,
        "description": "고혈압 환자이며 새우 알러지가 있습니다."
    },
    "2": {
        "user_id": "2",
        "name": "투석 전 신장질환 환자 (70kg)",
        "restricted_ingredients": [],
        "protein": 42.0,
        "sodium": 2300.0,
        "phosphorus": 1000.0,
        "calcium": 1000.0,
        "kcal": 2450.0,
        "description": "투석 전 신장질환 환자입니다. 단백질 및 나트륨 섭취를 제한해야 합니다."
    },
    "3": {
        "user_id": "3",
        "name": "투석 중 신장질환 + 밀 알러지 환자",
        "restricted_ingredients": ["밀"],
        "protein": 84.0,
        "sodium": 2300.0,
        "potassium": 2000.0,
        "phosphorus": 1000.0,
        "kcal": 2450.0,
        "description": "투석 중인 신장질환 환자이며 밀 알러지가 있습니다."
    },
    "4": {
        "user_id": "4",
        "name": "당뇨 + 고혈압 복합 환자",
        "restricted_ingredients": [],
        "sugar": 5.0,
        "sodium": 2300.0,
        "potassium_min": 3500.0,
        "fat_ratio": 0.25,
        "description": "당뇨와 고혈압을 모두 가진 복합 질환 환자입니다."
    },
    "5": {
        "user_id": "5",
        "name": "복합 알러지 환자 (유제품, 계란, 견과류)",
        "restricted_ingredients": ["우유", "계란", "견과류"],
        "is_allergy_only": True,
        "description": "유제품, 계란, 견과류에 복합 알러지가 있습니다."
    }
}

allergy_substitution_rules = {
    "우유": {
        "substitutes": ["두유", "아몬드유", "오트유", "쌀음료", "코코넛밀크"],
        "tip": "크리미한 질감을 원할 경우 코코넛밀크나 캐슈넛 밀크가 적합합니다."
    },
    "땅콩": {
        "substitutes": ["해바라기씨", "호박씨", "캐슈넛", "병아리콩"],
        "tip": "고소한 맛은 볶은 씨앗류나 콩류로 대체 가능합니다."
    },
    "밀": {
        "substitutes": ["쌀가루", "귀리가루", "타피오카 가루", "메밀가루"],
        "tip": "글루텐 프리 가루 믹스를 사용하여 점성을 조절하세요."
    },
    "새우": {
        "substitutes": ["흰살 생선", "버섯(킹오이스터)", "두부"],
        "tip": "탱글한 식감은 버섯이나 어묵으로 대체합니다."
    },
    "계란": {
        "substitutes": ["두부", "병아리콩 거품", "치아씨드 페이스트", "강낭콩"],
        "tip": "베이킹 시 계란의 결합력은 아쿠아파바나 바나나로 대체 가능합니다."
    },
    "대두": {
        "substitutes": ["완두콩", "병아리콩", "코코넛 아미노스", "퀴노아"],
        "tip": "간장 대신 코코넛 아미노스를 사용하면 대두 없이 감칠맛을 낼 수 있습니다."
    }
}

# ============== API 모델 ==============

class AnalysisRequest(BaseModel):
    product_id: str
    profile_id: str

class AnalysisResponse(BaseModel):
    product_name: str
    profile_name: str
    allergen_detected: List[Dict[str, Any]]
    safety_status: str
    safety_summary: str
    recommendations: List[Dict[str, Any]]

# ============== API 엔드포인트 ==============

@app.get("/")
def read_root():
    return {
        "message": "AI-NutriCurator API Server",
        "version": "1.0.0",
        "endpoints": [
            "/products",
            "/profiles",
            "/analyze"
        ]
    }

@app.get("/products")
def get_products():
    """전체 제품 목록 조회"""
    return {"products": list(products.values())}

@app.get("/products/{product_id}")
def get_product(product_id: str):
    """특정 제품 상세 조회"""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": products[product_id]}

@app.get("/profiles")
def get_profiles():
    """전체 사용자 프로필 목록 조회"""
    return {"profiles": list(final_profiles.values())}

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: str):
    """특정 사용자 프로필 조회"""
    if profile_id not in final_profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"profile": final_profiles[profile_id]}

@app.post("/analyze")
def analyze_product(request: AnalysisRequest):
    """제품 알러지 분석"""
    product_id = request.product_id
    profile_id = request.profile_id
    
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    if profile_id not in final_profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    product = products[product_id]
    profile = final_profiles[profile_id]
    
    # 알러지 성분 검출
    allergen_detected = []
    restricted = profile.get("restricted_ingredients", [])
    
    # 제품의 알러지 정보 파싱
    product_allergens = []
    if product["allergy"] and product["allergy"] != "없음" and product["allergy"] != "알수없음":
        product_allergens = [a.strip() for a in product["allergy"].split(",")]
    
    # 원재료에서 알러지 성분 검출
    ingredients = product.get("ingredients", [])
    
    for restricted_item in restricted:
        # 제품 알러지 정보에 있는 경우
        if any(restricted_item in allergen for allergen in product_allergens):
            allergen_info = {
                "ingredient": restricted_item,
                "severity": "critical",
                "source": "제품 알러지 표기",
                "detected_in": product["allergy"]
            }
            allergen_detected.append(allergen_info)
        # 원재료에 직접 포함된 경우
        elif any(restricted_item in ing for ing in ingredients):
            matching_ingredients = [ing for ing in ingredients if restricted_item in ing]
            allergen_info = {
                "ingredient": restricted_item,
                "severity": "critical",
                "source": "원재료 목록",
                "detected_in": ", ".join(matching_ingredients)
            }
            allergen_detected.append(allergen_info)
    
    # 교차오염 검사
    trace_warning = None
    if product["trace"] and product["trace"] != "null":
        for restricted_item in restricted:
            if restricted_item in product["trace"]:
                trace_warning = {
                    "ingredient": restricted_item,
                    "severity": "warning",
                    "source": "교차오염 가능",
                    "detected_in": product["trace"]
                }
                allergen_detected.append(trace_warning)
    
    # 안전성 판정
    if allergen_detected:
        critical_allergens = [a for a in allergen_detected if a["severity"] == "critical"]
        if critical_allergens:
            safety_status = "danger"
            safety_summary = f"⚠️ 위험: 알러지 성분({', '.join([a['ingredient'] for a in critical_allergens])})이 포함되어 있습니다. 섭취를 피하세요."
        else:
            safety_status = "warning"
            safety_summary = f"⚠️ 주의: 교차오염 가능성이 있습니다. 주의가 필요합니다."
    else:
        safety_status = "safe"
        safety_summary = "✅ 안전: 알려진 알러지 성분이 검출되지 않았습니다."
    
    # 대체재 추천
    recommendations = []
    for allergen in allergen_detected:
        if allergen["severity"] == "critical":
            ingredient = allergen["ingredient"]
            if ingredient in allergy_substitution_rules:
                rule = allergy_substitution_rules[ingredient]
                recommendations.append({
                    "allergen": ingredient,
                    "substitutes": rule["substitutes"],
                    "tip": rule["tip"]
                })
    
    return {
        "product_name": product["name"],
        "profile_name": profile["name"],
        "allergen_detected": allergen_detected,
        "safety_status": safety_status,
        "safety_summary": safety_summary,
        "recommendations": recommendations
    }

@app.get("/search")
def search_products(q: Optional[str] = None, category: Optional[str] = None):
    """제품 검색"""
    results = list(products.values())
    
    if q:
        q_lower = q.lower()
        results = [p for p in results if q_lower in p["name"].lower() or 
                   any(q_lower in ing.lower() for ing in p["ingredients"])]
    
    if category:
        results = [p for p in results if p["category"] == category]
    
    return {"results": results, "count": len(results)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
