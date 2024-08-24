FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/
COPY ./mini /app/mini

RUN mkdir -p /app/data
RUN pip install --no-cache-dir --upgrade --requirement /app/requirements.txt

CMD ["fastapi", "run", "mini/app.py", "--port", "80", "--reload"]
