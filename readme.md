# Activity Feed System

## Background

For any social network, activity feed is a common feature that usually starts off simple to implement but can grow in complexity as the number of users increases. This can cause performance issues that can cripple user experience.

## Requirements

- docker
- docker-compose
- Python 3
- Timescaledb

## Installation

```
docker-compose up
# And wait for complete
curl -X GET http://localhost:5000/me -H 'X-App-Key: abc123'

{"id": 1, "name": "ivan", "auth_token": "abc123", "follow_ids": [2], "created_at": "Sun, 10 Feb 2019 09:47:03 GMT", "updated_at": "Sun, 10 Feb 2019 09:47:03 GMT"}
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

## API

### 1. Why separating `post` and `follow` from endpoints /activity ?

## Architecture

### 1. Why timescaledb?


## Todo