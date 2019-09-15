import os
import json

def getenv_or_none(name: str) -> str:
    return os.getenv(name) if (name in os.environ and os.getenv(name) != '') else None

config = dict({
    'url': os.getenv('RABBIT_MQ_URL', 'amqp://taiga:taiga_pw@rabbitmq:5672/taiga'),
    'secret': os.getenv('SECRET_KEY'),
    'webSocketServer': {
        'port': 8888
    }
})

print(json.dumps(config))