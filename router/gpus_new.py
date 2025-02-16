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

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]


class Gpus(BaseModel):
    name: str = Field(min_length=4)
    description: str = Field(min_length=5, max_length=50)
    has_dlss: bool


@router.get("/gpus", status_code=status.HTTP_200_OK)
async def get_gpus(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Gpus).filter(models.Gpus.owner_id==user.get("user_id")).all()

@router.get("/gpus/{id}", status_code=status.HTTP_200_OK)
async def get_gpus(user: user_dependency, db: Annotated[Session, Depends(get_db)], id: int = Path(gt=0)):
    gpu = db.query(models.Gpus).filter(models.Gpus.id == id).filter(models.Gpus.owner_id==user.get("user_id")).first()
    if gpu is not None:
        return gpu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gpu not found")

@router.post("/gpus", status_code=status.HTTP_201_CREATED)
async def create_gpus(user: user_dependency, db: db_dependency, gpu: Gpus):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    created_gpu = models.Gpus(**gpu.model_dump(), owner_id=user.get('user_id'))

    db.add(created_gpu)
    db.commit()

@router.put("/gpus/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_gpus(user: user_dependency, db: db_dependency, gpu: Gpus, id: int = Path(gt=0)):
    db_gpu = db.query(models.Gpus).filter(models.Gpus.id == id).filter(models.Gpus.owner_id==user.get("user_id")).first()
    if db_gpu:
        db_gpu.name = gpu.name
        db_gpu.description = gpu.description
        db_gpu.has_dlss = gpu.has_dlss
        db.add(db_gpu)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No gpu found") 
    
@router.delete("/gpus/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gpu(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    db_gpu = db.query(models.Gpus).filter(models.Gpus.id == id).filter(models.Gpus.owner_id==user.get("user_id")).first()
    if db_gpu:
        db.query(models.Gpus).filter(models.Gpus.id == id).filter(models.Gpus.owner_id==user.get("user_id")).delete()
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No gpu found") 
