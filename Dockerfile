FROM python:3.12-slim AS backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p data/uploads data/chroma

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM node:20-alpine AS frontend

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/frontend/dist
COPY main.py config.py requirements.txt ./
RUN mkdir -p data/uploads data/chroma

ENV APP_ENV=production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
