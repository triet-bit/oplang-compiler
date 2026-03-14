import os
import subprocess
import uuid
import shutil
import glob
from celery import Celery


REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
celery = Celery(
    'compiler_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)
BASE_DIR = "/app"
TEMP_DIR = "/app/temp"
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
        cmd = ["python", "compiler_main.py", input_file_path, output_file_path]        
        process = subprocess.run(
            cmd,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=10
        )
        if process.returncode != 0:
            # Nếu run.py báo lỗi (VD: lỗi cú pháp python, thiếu thư viện...)
            result_data["status"] = "system_error"
            result_data["error"] = process.stderr
        else:
            # Đọc file result.txt xem Compiler trả về gì
            if os.path.exists(output_file_path):
                with open(output_file_path, "r") as f:
                    output_content = f.read()
                
                # Logic: Nếu result có chữ "Error" thì là lỗi biên dịch
                # Nếu không thì là chạy thành công
                if "Error" in output_content or "Runtime error" in output_content:
                    result_data["status"] = "compilation_error"
                    result_data["error"] = output_content
                else:
                    result_data["status"] = "success"
                    result_data["output"] = output_content
            else:
                result_data["status"] = "error"
                result_data["error"] = "No output file generated"

    except subprocess.TimeoutExpired:
        result_data["status"] = "timeout"
        result_data["error"] = "Compilation/Execution timed out (10s)"
    except Exception as e:
        result_data["status"] = "internal_error"
        result_data["error"] = str(e)
    finally:
        # Dọn dẹp file rác
        shutil.rmtree(job_dir, ignore_errors=True)
        
    return result_data