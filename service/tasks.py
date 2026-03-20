import os
import subprocess
import uuid
import shutil
import glob
import sys
from celery import Celery

sys.path.insert(0, "/app")
from compiler_main import main as compiler_main

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
celery = Celery(
    'compiler_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)
BASE_DIR = "/app"
TEMP_DIR = "/app/temp_jobs"
@celery.task
def compile_and_run(source_code: str): 
    # tao ra id duy nhat 
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(TEMP_DIR,job_id)
    os.makedirs(job_dir,exist_ok=True)

    input_file_path = os.path.join(job_dir,"input.txt")
    output_file_path = os.path.join(job_dir,"output.txt")
    with open(input_file_path,"w") as f: 
        f.write(source_code)
    
    result_data = {
        "status": "pending", 
        "output": "", 
        "error": ""
    }
    try: 
        compiler_main(input_file_path, output_file_path)

        if os.path.exists(output_file_path):
            with open(output_file_path, "r") as f:
                output_content = f.read()
            if "Error" in output_content:
                result_data["status"] = "compilation_error"
                result_data["error"] = output_content
            else:
                result_data["status"] = "success"
                result_data["output"] = output_content
        else:
            result_data["status"] = "error"
            result_data["error"] = "No output file generated"
    except TimeoutError:
        result_data["status"] = "timeout"
        result_data["error"] = "Timed out after 10s"
    except Exception as e:
        result_data["status"] = "compilation_error" # syntax, semantic errors
        result_data["error"] = str(e)
    finally:
        shutil.rmtree(job_dir, ignore_errors=True)
        
    return result_data