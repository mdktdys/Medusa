FROM tiangolo/uvicorn-gunicorn:python3.11-slim

RUN apt-get update && \
    apt-get install -y libmagic1 libmagic-dev libgl1-mesa-glx libglib2.0-0

ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
