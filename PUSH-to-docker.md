# Internal documentation

This is only the internal documentation on how to push this image to docker hub.

```bash
git pull
docker build . \
-t docker-taiga:latest \
-t taiq/docker-taiga:latest \
-t taiq/docker-taiga:4 \
-t taiq/docker-taiga:4.2 \
-t taiq/docker-taiga:4.2.12 \
-t taiq/docker-taiga:4.2.12_1

docker push taiq/docker-taiga
```