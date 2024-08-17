FROM tiangolo/uvicorn-gunicorn:python3.11-slim

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["dir"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
