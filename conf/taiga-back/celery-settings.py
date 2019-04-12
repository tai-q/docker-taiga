import os
broker_url = os.getenv('RABBIT_MQ_URL', 'amqp://taiga:taiga_pw@rabbitmq:5672/taiga')
result_backend = os.getenv('REDIS_URL', 'redis://redis:6379/0')