# from fastapi import APIRouter, Form, Request, Depends
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app import models
# import google.generativeai as genai  # və ya istifadə etdiyin Gemini SDK
#
# router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")
#
# # Gemini API konfiqurasiyası
# genai.configure(api_key="AIzaSyCCbA9QSAVADwas0_ev9vd_qZOBF0UPDro")
#
# # DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @router.post("/analyze", response_class=HTMLResponse)
# def analyze(
#     request: Request,
#     name: str = Form(...),
#     description: str = Form(None),
#     db: Session = Depends(get_db)
# ):
#     # 1️⃣ Yeni item yaradılır
#     item = models.Item(name=name, description=description)
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#
#     # 2️⃣ Gemini prompt
#     prompt = (
#         f"Söz: {name}\n"
#         f"Təsvir: {description or ''}\n\n"
#         "Bu sözü verdiyim cümlə kontekstinə görə (əgər varsa) təhlil et. "
#         "Nitq hissəsini müəyyən et, hallanmasını göstər, mənasını izah et. "
#         "Eyni zamanda təsvir kontekstinə əsaslanaraq (əgər varsa) sözün düzgün funksiyasını (isim, fel, sifət və s.) göstər. "
#         "Azərbaycan dilində, oxunaqlı və nümunələrlə izah et."
#         "Maraqlı və fəlsəfi cümlədə işlət"
#     )
#
#     try:
#         model = genai.GenerativeModel('gemini-2.0-flash-lite')
#         response = model.generate_content(prompt)
#         analysis_text = response.text
#     except Exception as e:
#         analysis_text = f"Xəta: {e}"
#
#     # 3️⃣ DB update
#     item.analysis = analysis_text
#     db.commit()
#     db.refresh(item)
#
#     # 4️⃣ HTML render
#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request, "analysis": analysis_text, "name": name, "description": description}
#     )
#
#
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()  # .env faylını cari qovluqdan oxuyur


gemini_api_key = os.getenv("gemini_api_key")


router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Gemini API konfiqurasiyası
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

@router.post("/analyze")
async def analyze(data: dict, db: Session = Depends(get_db)):
    name = data.get("name")
    description = data.get("description", "")

    # DB-də yeni item
    item = models.Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)

    # Prompt
    prompt = (
        "Sən filoloji təhlil redaktorusan."
        f"Söz: {name}\n"
        f"Cümlə konteksti: {description or ''}\n\n"
        "1. Bu sözü verdiyim cümlə kontekstinə görə (əgər varsa) təhlil et. "
        "2. Nitq hissəsini müəyyən et. "
        "3. Hallandır. "
        "4. Mənasını izah et. "
        "5. Əgər söz şəkilçi ilə işlənibsə, şəkilçilərin hər birini ayrıca izah et. "
        "6. Eyni zamanda təsvir kontekstinə əsaslanaraq (əgər varsa) sözün düzgün funksiyasını (isim, fel, sifət və s.) göstər. "
        "7. Azərbaycan dilində, oxunaqlı nümunələrlə izah et. "
        "8. Azərbaycan ədəbiyyatından 5 cümlə və müəllif və əsərin adını yaz. "
        "Xahiş edirəm əvvəldə 'Söz'-ü və 'Cümlə konteksti'-ni də yaz. Yuxarıdakı ardıcıllıqda cavab ver və **-lar işlətmə"
    )

    try:
        response = model.generate_content(prompt)
        analysis_text = response.text.strip()  # Burada .text istifadə olunur
    except Exception as e:
        analysis_text = f"Xəta: {e}"

    # DB update
    item.analysis = analysis_text
    db.commit()
    db.refresh(item)

    return JSONResponse(content={"analysis": analysis_text})
