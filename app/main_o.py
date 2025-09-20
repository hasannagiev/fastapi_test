#
# from . import models, schemas, database
# from fastapi import FastAPI, Request, Depends
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from . import models, database
# from fastapi.staticfiles import StaticFiles  # <-- əlavə et
#
#
# app = FastAPI(title="FastAPI + PostgreSQL demo")
#
# # static fayllar üçün
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
#
#
# templates = Jinja2Templates(directory="app/templates")
#
# # DB yarat
# models.Base.metadata.create_all(bind=database.engine)
#
# # DB session dependency
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# # @app.get("/")
# # def read_root():
# #     return {"message": "Salam, FastAPI + SQLite!"}
#
#
# # # Startup event ilə test item
# # @app.on_event("startup")
# # def startup_populate_db():
# #     db: Session = database.SessionLocal()
# #     if not db.query(models.Item).first():
# #         db.add(models.Item(name="söz", description="başa düşmək üçün"))
# #         db.add(models.Item(name="cümlə", description="başa düşmək üçün"))
# #         db.commit()
# #     db.close()
#
# # Create item
# @app.post("/items/", response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     db_item = models.Item(name=item.name, description=item.description)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
#
# # Read items (API)
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
# # JSON API
# @app.get("/api/items")
# def read_items_api(db: Session = Depends(get_db)):
#     return db.query(models.Item).all()
#
# # HTML səhifə
# @app.get("/", response_class=HTMLResponse)
# def read_index(request: Request, db: Session = Depends(get_db)):
#     items = db.query(models.Item).all()
#     return templates.TemplateResponse("index.html", {"request": request, "items": items})


from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/items/create")
def create_item(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    new_item = models.Item(name=name, description=description)
    db.add(new_item)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/items/update/{item_id}")
def update_item(item_id: int, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = name
    db_item.description = description
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/items/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
