from typing import Annotated
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from datetime import datetime
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
# from fastapiproject.models import Gpus as ModelGpus

# from fastapiproject.main import get_db

app = FastAPI()

class Gpus():
    name: str
    cuda_count: int
    tgp: str

    def __init__(self, name, cuda_count, tgp) -> None:
        self.name = name 
        self.cuda_count = cuda_count
        self.tgp = tgp

        
class GpusRequest(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    cuda_count: int = Field(gt=0, lt=10000)
    tgp: str = Field(min_length=3, max_length=5)




@app.get("/gpus/{name}")
async def get_cheap_gpus(name: str = Path(min_length=3), cheap: bool = Query(len=4)):
    return {"message": f"{name} is {'cheap' if cheap else 'expensive'}"}


@app.post("/gpus/add_gpu/")
async def add_gpu(name = Body()):
    return {"message": f"Created: {name.get("name")}"}


@app.put("/gpus/update_gpu/")
async def add_gpu(name = Body()):
    return {"message": f"Updated: {name.get("name")}"}


@app.delete("/gpus/delete/{deleting_gpu}/")
async def add_gpu(deleting_gpu: str):
    return {"message": f"Deleted: {deleting_gpu}"}


@app.post("/gpus/from/pydantic/")
async def add_gpu_with_validation(gpu: GpusRequest):
    gpu = Gpus(**gpu.model_dump())
    if not gpu:
        raise HTTPException(status_code=422, detail="Unprocessable")
    return {"message": f"Added {gpu} of type: {type(gpu)}"}