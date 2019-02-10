docker exec -it activity_web_1 cat test_basic.sh
docker exec -it activity_web_1 sh test_basic.sh
docker cp activity_web_1:/usr/src/app/cover ./cover_basic

docker exec -it activity_web_1 cat test_advance.sh
docker exec -it activity_web_1 sh test_advance.sh
docker cp activity_web_1:/usr/src/app/cover ./cover_advance

ls -ahl | grep cover