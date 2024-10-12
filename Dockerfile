FROM tiangolo/uvicorn-gunicorn:python3.11-slim

RUN apt-get update && \
      apt-get install -y libmagic1 libmagic-dev && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN pip install celery

CMD uvicorn main:app --host 0.0.0.0 --port 5000 & celery -A src.parser.tasks worker --loglevel=INFO --pool=solo
