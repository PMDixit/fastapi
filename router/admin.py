from curses.ascii import HT
from fastapi import FastAPI
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from typing import Annotated
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from router import auth
from fastapi import APIRouter
from models import Gpus

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get('/gpus', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Gpus).all()

@router.delete("/gpu/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gpu(user: user_dependency, db: db_dependency, id:int = Path(gt=0)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    gpu = db.query(Gpus).filter(Gpus.id == id)
    if not gpu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gpu not found")
    else:
        gpu.delete()
        db.commit()