from celery import Celery

fastapi_celery_app = Celery(
    "fastapi",
    broker="amqp://guest:guest@rabbitmq:5672//",  # Используйте 127.0.0.1 для RabbitMQ
    backend="redis://redis:6379/0",  # Используйте 127.0.0.1 для Redis
)

API_TOKEN = "7283968288:AAHB_Z9-NeXSdgwvYbikLMoX4Kv5z-fdBVw"

print("***")
print(fastapi_celery_app.tasks.keys())
print("***")
