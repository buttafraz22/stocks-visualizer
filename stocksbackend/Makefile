makemigration:
	python manage.py makemigrations
migrate: makemigration
	python manage.py migrate

static: migrate
	python manage.py collectstatic

run: migrate
	python manage.py runserver 0.0.0.0:8000
up:
	docker-compose up
down:
	docker-compose down

build:
	docker-compose build

redis-up:
	redis-server --save 20 1 --loglevel warning --requirepass eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81

celery-beat:
	celery -A stocksbackend beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

celery-worker:
	celery -A stocksbackend worker --loglevel=info

run-test:
	pytest -v -s