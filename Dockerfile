FROM python:3.12-slim

# 'rm -rf /var/lib/apt/lists/*' giúp giảm dung lượng image
RUN apt-get update && \
    apt-get install -y default-jre-headless default-jdk-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python run.py build

RUN javac src/runtime/io.java

ENV PYTHONPATH=/app
ENV CLASSPATH=".:/app/external/antlr-4.13.2-complete.jar:/app/src/runtime/jasmin.jar:/app/src/runtime"

RUN useradd -m -u 1000 oplang_user

RUN mkdir -p /app/temp_jobs && \
    chown -R oplang_user:oplang_user /app

USER oplang_user

CMD ["python", "compiler_main.py"]