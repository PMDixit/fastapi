from fastapi import FastAPI
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from typing import Annotated
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from router import auth, gpus_new, admin

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(gpus_new.router)
app.include_router(admin.router)
