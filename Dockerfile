FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home shop && chown -R shop:shop /app
USER shop
EXPOSE 8000
CMD ["sh", "-c", "python scripts/generate_initial_catalog.py && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]

