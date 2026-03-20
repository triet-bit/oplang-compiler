from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from service.tasks import compile_and_run, celery
from celery.result import AsyncResult
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import glob
import os
import shutil
import sys
import tempfile
app = FastAPI(title="OPLang Compiler")

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
@app.get('/result/{task_id}')
def get_results(task_id: str): 
    # khi goi AsyncResult ph de them app=_, de no biet dc duong den redis
    task_result = AsyncResult(task_id,app=celery)
    if not task_result.ready(): 
        return {"status": "pending"}
    return {
        "status": "completed", 
        "data": task_result.result
    }
# ── Interactive WebSocket endpoint ──
RUNTIME_DIR = "/app/src/runtime"
 
@app.websocket("/ws/run")
async def websocket_run(ws: WebSocket):
    await ws.accept()
    job_dir = tempfile.mkdtemp(dir="/app/temp_jobs")
 
    try:
        # 1. Nhận source code từ browser
        data = await asyncio.wait_for(ws.receive_json(), timeout=10)
        source_code = data.get("source_code", "")
 
        await ws.send_json({"type": "status", "msg": "Compiling..."})
 
        # 2. Chạy compiler_main để compile → .class files
        input_path = os.path.join(job_dir, "input.opl")
        out_path = os.path.join(job_dir, "out.txt")
 
        with open(input_path, "w") as f:
            f.write(source_code)
 
        comp = await asyncio.create_subprocess_exec(
            sys.executable, "compiler_main.py", input_path, out_path,
            cwd="/app",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            _, stderr = await asyncio.wait_for(comp.communicate(), timeout=20)
        except asyncio.TimeoutError:
            comp.kill()
            await ws.send_json({"type": "error", "msg": "Compilation timed out"})
            return
 
        if comp.returncode != 0:
            await ws.send_json({"type": "error", "msg": stderr.decode() or "Compilation failed"})
            return
 
        # Check output file cho compiler errors
        if os.path.exists(out_path):
            content = open(out_path).read()
            if "Error" in content:
                await ws.send_json({"type": "error", "msg": content})
                return
 
        # 3. Tìm main class trong runtime dir
        main_class = None
        for jf in glob.glob(os.path.join(RUNTIME_DIR, "*.j")):
            try:
                with open(jf) as f:
                    if ".method public static main" in f.read():
                        main_class = os.path.basename(jf).replace(".j", "")
                        break
            except Exception:
                pass
 
        if not main_class:
            await ws.send_json({"type": "error", "msg": "No main class found"})
            return
 
        await ws.send_json({"type": "status", "msg": "Running..."})
 
        # 4. Spawn JVM process với stdin/stdout pipe
        proc = await asyncio.create_subprocess_exec(
            "java", main_class,
            cwd=RUNTIME_DIR,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
 
        # 5. Stream output + nhận input đồng thời bằng asyncio.gather
        done_event = asyncio.Event()

        async def stream_stdout():
            """Đọc stdout của JVM và gửi về browser"""
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                await ws.send_json({"type": "output", "msg": line.decode()})
            done_event.set()  # báo JVM stdout đã xong
        async def stream_stderr():
            """Đọc stderr của JVM và gửi về browser"""
            while True:
                line = await proc.stderr.readline()
                if not line:
                    break
                await ws.send_json({"type": "stderr", "msg": line.decode()})
 
        async def receive_input():
            """Nhận input từ browser và đẩy vào stdin của JVM"""
            while True:
                if done_event.is_set():
                    break
                try:
                    msg = await asyncio.wait_for(ws.receive_json(), timeout=0.5)
                    if msg.get("type") == "input":
                        user_input = msg["msg"] + "\n"
                        proc.stdin.write(user_input.encode())
                        await proc.stdin.drain()
                    elif msg.get("type") == "kill":
                        proc.kill()
                        break
                except asyncio.TimeoutError:
                    continue  # timeout ngắn chỉ để check done_event, không kill
                except (WebSocketDisconnect, Exception):
                    proc.kill()
                    break
 
        # Chạy đồng thời 3 coroutine
        await asyncio.gather(
            stream_stdout(),
            stream_stderr(),
            receive_input(),
            return_exceptions=True
        )
 
        await proc.wait()
        await ws.send_json({"type": "done", "code": proc.returncode})
 
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "msg": str(e)})
        except Exception:
            pass
    finally:
        shutil.rmtree(job_dir, ignore_errors=True)
 
 
static_dir = os.path.join(os.path.dirname(__file__),"static")
app.mount("/static",StaticFiles(directory=static_dir),name="static")
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

