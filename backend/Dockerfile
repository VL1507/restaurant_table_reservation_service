FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip 
RUN pip install --no-cache-dir uv

COPY uv.lock pyproject.toml /backend/

RUN uv sync

COPY ./app/ /backend/app/

EXPOSE 8000

# CMD [ "uv", "run", "uvicorn", "app.main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]