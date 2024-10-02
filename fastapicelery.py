from celery import Celery

fastapi_celery_app = Celery(
    "fastapi",
    broker="amqp://guest:guest@rabbitmq:5672//",  # Используйте 127.0.0.1 для RabbitMQ
    backend="redis://redis:6379/0",  # Используйте 127.0.0.1 для Redis
)
