from fastapi import FastAPI
from pydantic import BaseModel
from service.tasks import compile_and_run, celery
from celery.result import AsyncResult
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse  
import os
app = FastAPI(title="OPLang Compiler Service")

class Submission(BaseModel): 
    source_code: str 

@app.post('/submit')
def submit(request: Submission): 
    # day task vai hang doi redis
    task = compile_and_run.delay(request.source_code)
    return {
        "task_id": task.id, 
        "status": "queued"
    }
@app.get('/status/{task_id}')
def get_results(task_id: str): 
    # khi goi AsyncResult ph de them app=_, de no biet dc duong den redis
    task_result = AsyncResult(task_id,app=celery)
    if not task_result.ready(): 
        return {"status": "pending"}
    return {
        "status": "completed", 
        "data": task_result.result
    }
static_dir = os.path.join(os.path.dirname(__file__),"static")
app.mount("/static",StaticFiles(directory=static_dir),name="static")
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))