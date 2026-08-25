FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && addgroup --system app && adduser --system --ingroup app app
COPY backend backend
COPY scripts scripts
RUN mkdir -p /app/data /app/products/approved /app/products/generated /app/products/rejected && chown -R app:app /app
USER app
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000"]
