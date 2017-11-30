.PHONY: shell runserver migrate collectstatic graphql_schema test

shell:
	python manage.py shell

runserver:
	python manage.py runserver 0.0.0.0:8010

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --link --noinput

graphql_schema:
	python manage.py graphql_schema --schema config.schema.schema --out schema.json

lint:
	isort --recursive --diff .
	yapf --recursive --parallel --diff --exclude "*/snapshots/*" --exclude "*/migrations/*" .

clean:
	isort --recursive .
	yapf --recursive --parallel --in-place --exclude "*/snapshots/*" --exclude "*/migrations/*" .

test:
	pytest

coverage:
	pytest --cov=klasse
