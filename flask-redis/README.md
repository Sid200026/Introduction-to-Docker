```docker
docker-compose build
docker-compose up -d
```

Docker Compose will create a network between web and redis for us. The containers web and redis can communicate with each other via the names ie. web can communicate with redis using 'redis'. In a normal application, we use this

```py
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

We see that the host is localhost. However in docker, the web application can communicate with the redis via it's name. So we have

```py
import redis
r = redis.Redis(host='redis', port=6379, db=0)
```

```docker
version: "3.8"

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        PYTHON_VERSION: 3.9.0-alpine
    image: sid200026/flask-redis
    ports:
      - 5000:5000
    volumes:
      - .:/app
  redis:
    image: redis:6.0.8-alpine
```

### Utility Commands

```
docker-compose logs -f
docker-compose logs -f web
docker-compose stop
docker-compose start
```

Docker-Compose also provides us with a feature called `variable substitution` which allows us to specify a `.env` file from which Docker-Compose can reference variables. Docker-Compose has the ability to pick up .env files present in the same directory.
