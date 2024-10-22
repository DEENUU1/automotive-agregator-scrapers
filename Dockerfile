FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN addgroup --system app && adduser --system --group app

COPY app/config /app/config

COPY .env /app/.env

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]