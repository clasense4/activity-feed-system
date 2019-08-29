# Activity Feed System

## Background

For any social network, activity feed is a common feature that usually starts off simple to implement but can grow in complexity as the number of users increases. This can cause performance issues that can cripple user experience.

## Requirements

- docker
- docker-compose
- Python 3
- TimescaleDB

## Installation

```
cd ~
git clone https://github.com/clasense4/activity-feed-system.git
cd activity-feed-system
docker-compose up -d
# Or remove `-d`
sh test.sh
# And wait for complete
curl -X GET http://localhost:5000/me -H 'X-App-Key: abc123'

{"id": 1, "name": "ivan", "auth_token": "abc123", "follow_ids": [2], "created_at": "Sun, 10 Feb 2019 09:47:03 GMT", "updated_at": "Sun, 10 Feb 2019 09:47:03 GMT"}
```

## Docker & Docker Compose Ubuntu 18.04

```
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update  -y
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo systemctl status docker
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker --version
docker-compose --version
```

## Test

```
# On your local machine
sh test.sh
```

The script will create new 2 coverage directory on your local machine. Open `cover_basic/index.html` and `cover_advance/index.html` to see the result.

---

# Endpoints

## Authorization & Demo User

Use key `X-App-Key` at header to be authorized.

Example user :

- `abc123` -> Ivan
- `abc124` -> Nico
- `abc125` -> Eric


## GET /me

Description :

This endpoint will return the details of current user

Example :

```
curl -X GET http://localhost:5000/me -H 'X-App-Key: abc123'

{"id": 1, "name": "ivan", "auth_token": "abc123", "follow_ids": [2], "created_at": "Sun, 10 Feb 2019 09:47:03 GMT", "updated_at": "Sun, 10 Feb 2019 09:47:03 GMT"}
```

## POST /post

Description :

This endpoint can create `post` and `photo` activity. And it will add a record to `activities` table.

Example :

```
curl -X POST \
  http://localhost:5000/post \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{"type":"post","content":"foobar"}'

{
    "type": "post",
    "object_id": 22,
    "message": "Activity recorded"
}
```

```
curl -X POST \
  http://localhost:5000/post \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{"type":"photo","content":"photos1.jpeg"}'

{
    "type": "photo",
    "object_id": 22,
    "message": "Activity recorded"
}
```

## POST /activity

Description :

This endpoint can create `like` and `share` activity. And it will add a record to `activities` table. Knowing object is required. `object_id` is retrieved from POST /post endpoint.

Example :

```
curl -X POST \
  http://localhost:5000/activity \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{
    "verb":"share",
    "object":"photo:21"
}'

{
    "verb": "share",
    "message": "Activity recorded"
}
```

```
curl -X POST \
  http://localhost:5000/activity \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{
    "verb":"like",
    "object":"photo:21"
}'

{
    "verb": "like",
    "message": "Activity recorded"
}
```

## GET /feed/my

Description :

This endpoint will return user activity

Example :

```
curl -X GET \
  http://localhost:5000/feed/my \
  -H 'X-App-Key: abc123'

{
    "my_feed": [
        {
            "actor_name": "ivan",
            "verb": "post",
            "object_id": 21,
            "object_type": "photo",
            "target_name": null,
            "time": "2019-02-10T12:01:30.894037+00:00"
        },
        {
            "actor_name": "ivan",
            "verb": "unfollow",
            "object_id": null,
            "object_type": null,
            "target_name": "eric",
            "time": "2019-02-10T12:00:46.581562+00:00"
        }
    ],
    "next_url": ""
}
```

## GET /feed/friends

Description :

This endpoint will return friends (followed another user) activity

Example :

```
curl -X GET \
  http://localhost:5000/feed/friends \
  -H 'X-App-Key: abc123'

{
    "friends_feed": [
        {
            "actor_name": "nico",
            "verb": "post",
            "object_id": 20,
            "object_type": "photo",
            "target_name": null,
            "time": "Sun, 10 Feb 2019 13:04:22 GMT"
        },
        {
            "actor_name": "nico",
            "verb": "post",
            "object_id": 19,
            "object_type": "photo",
            "target_name": null,
            "time": "Sun, 10 Feb 2019 13:04:22 GMT"
        }
    ],
    "next_url": ""
}
```

## POST /follow

Description :

Use this endpoint to follow a user

Example :

```
curl -X POST \
  http://localhost:5000/follow \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{"follow":"eric"}'

{
    "verb": "follow",
    "message": "User followed"
}
```

## POST /unfollow

Description :

Use this endpoint to unfollow a user

Example :

```
curl -X POST \
  http://localhost:5000/follow \
  -H 'Content-Type: application/json' \
  -H 'X-App-Key: abc123' \
  -d '{"unfollow":"eric"}'

{
    "verb": "unfollow",
    "message": "User unfollowed"
}
```

---

## FAQ

## API & Application

### 1. Why separating `post` and `follow` from endpoints /activity ?

Previously I made `/activity` endpoint to support 4 type of verbs : post, follow, like, share. Then I realize, if I want to use `verb:post` I need to know the `object_id` and made validation if for the object. So instead, I'm creating `/post` endpoint, with return created `object_id`.

As for `verb:follow`, writing to table `activities` is already taken care by `/follow` endpoints.

### 2. Which web framework you choose and why?

I use flask, it is simple and easy. If in next time flask is slowing, we can port this flask application to python3 async web framework, for example [sanic](https://github.com/huge-success/sanic) and [quart](https://gitlab.com/pgjones/quart). Of course the postgresql drive need to be changed to [aysncpg](https://magic.io/blog/asyncpg-1m-rows-from-postgres-to-python/).

### 3. Why are you using orator query builder instead of sqlalchemy core?

I tried sqlalchemy core, and it is harder than orator. Orator orm is similar with most of active record implementation like in php and ruby.

## Architecture

### 1. Why [timescaledb](https://www.timescale.com/)?

Timescaledb is a timeseries database, with fast ingest, and fast read especially specific data that related to time. Actually only table `activities` that can take advantage from timescale. So, for another table, it can be store at regular postgresql databases.

### 2. Are you not using any queue like celery or sqs?

I should use queue, especially when writing to table `activities`. But our activities table is in format time series and timescaledb is good at that. I think we can test its fast ingest as they advertised.

### 3. What is your plan on production?

Thanks to docker, we can host the web app using [ECS](https://aws.amazon.com/ecs/) or [EKS](https://aws.amazon.com/eks/). Or if there is too much differences on container, we can host it on elastic beanstalk, and create a custom platform using packer. 

Timescaledb v1.2 has new support, they provide [timescaledb ami](https://docs.timescale.com/v1.2/getting-started/installation/ami/installation-ubuntu-ami). But still need some improvement on postgre config.

## Improvement

### 1. Add a simple fake data generator.

The data that we working on should be very high, and it is needed.

### 2. Add load testing tools like : [locust](https://locust.io/).

This architecture is not proven yet until we attack our architecture. When we have baseline number, we can have a comparison.

### 3. Add Redis.

This part is still missing for now. Redis can be use for validation. For example, on `/follow` endpoints, instead of using query to check user is exists, we can use combination of [redis command](https://redis.io/commands#set) : `SADD` & `SISMEMBER` which given O(1) complexity.

And another example, on `/feed/my` or `/feed/friends` we can cache the query result via redis, and invalidate it for 30 seconds (or lower). Depends on our case, performance vs data validity.

Previously I have a plan to use [redis stream](https://redis.io/topics/streams-intro), but I have no proven experience for this new command and as I realized, this case is need at least warm data, so timescale (or RDBMS) is good choice.

