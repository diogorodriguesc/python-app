# How to

## Install and start

```
docker-compose -f docker/docker-compose.yml up
```

## Connect using docker instance

```
docker exec -it docker-database-1 bash
psql -d app -h 0.0.0.0 -U root -W
```

## Connect using Postgres Client

Host: 0.0.0.0
Port: 6543
User: root
Password: root
Database: app