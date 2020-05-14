makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser:
	docker-compose exec web python manage.py createsuperuser --username=superadmin --email=''

shell-plus:
	docker-compose exec web python manage.py shell_plus

init-user-groups:
	docker-compose exec web python manage.py init_user_groups

sql-login:
	docker-compose exec db mysql -u root -p

dockerlog-web:
	docker container logs absensi-lobar-web

dockerlog-db:
	docker container logs absensi-lobar-db

dockerlog-phpmyadmin:
	docker container logs absensi-lobar-phpmyadmin

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-restart:
	docker-compose down
	docker-compose up -d

docker-build:
	docker-compose build

docker-build-up:
	docker-compose build	
	docker-compose down
	docker-compose up -d

docker-up-prod:
	docker-compose -f docker-compose.prod.yml up -d

docker-down-prod:
	docker-compose -f docker-compose.prod.yml down

docker-build-prod:
	docker-compose -f docker-compose.prod.yml build