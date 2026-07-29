FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY scripts/ scripts/
COPY tasks/ tasks/
RUN adduser --disabled-password --gecos "" ambench
USER ambench
ENTRYPOINT ["python3", "src/harness.py"]
