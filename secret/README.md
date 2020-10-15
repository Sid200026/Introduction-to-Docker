```docker
docker build -t secret .  
docker run -v "$(pwd)":/app secret
```