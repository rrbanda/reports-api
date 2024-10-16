# Reports API

```
+-------------------+          +-------------------+
|                   |          |                   |
|   FastAPI App     | <------> |    MongoDB        |
|   (Podman)        |          |    (Podman)       |
|                   |          |                   |
+-------------------+          +-------------------+


```


## Build the api service container 

` podman build -t quay.io/rbrhssa/reports-api:latest . `

## Push the container to quay

` podman push quay.io/rbrhssa/reports-api:latest ` 


## Create Podman Network

` podman network create ai_network `




## To run mongodb

``` 
podman run -d \
  --name mongodb \
  --network ai_network \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=patient_db \
  mongo:latest ` 

```
## Run reports api as podman container

```
  podman run -d \
  --name reports_service \
  --network ai_network \
  -p 8000:8000 \
  --env-file app/.env \
  fastapi_service
  ```
