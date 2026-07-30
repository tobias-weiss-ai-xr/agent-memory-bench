FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 bench && \
    adduser --system --uid 1001 --ingroup bench bench && \
    chown bench:bench /app

# Copy and install deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ src/
COPY scripts/ scripts/
COPY tasks/ tasks/
COPY task-templates/ task-templates/

USER bench

ENTRYPOINT ["python", "-m", "src.harness"]
CMD ["--help"]
