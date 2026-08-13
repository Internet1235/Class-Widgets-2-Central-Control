FROM node:22-alpine AS frontend-build

WORKDIR /web
COPY web/package*.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY server/pyproject.toml ./
COPY server/app ./app
COPY server/migrations ./migrations
COPY server/alembic.ini ./
COPY --from=frontend-build /web/dist ./frontend-dist
RUN pip install --no-cache-dir .
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'"]
