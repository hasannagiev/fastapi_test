
from . import models, schemas, database
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI(title="FastAPI + SQLite demo")
templates = Jinja2Templates(directory="app/templates")

# DB yaradır (əgər yoxdursa)
models.Base.metadata.create_all(bind=database.engine)

# DB session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Salam, FastAPI + SQLite!"}

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Item).offset(skip).limit(limit).all()


# API endpoint
@app.get("/api/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

# HTML səhifə
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})