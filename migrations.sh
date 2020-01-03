docker-compose up -d --build
docker exec -it perdana-indonesia_web_1 python manage.py makemigrations --settings=config.prod_settings
docker exec -it perdana-indonesia_web_1 python manage.py migrate --settings=config.prod_settings
