.PHONY: shell runserver migrate collectstatic graphql_schema test

shell:
	pipenv run python manage.py shell

runserver:
	pipenv run python manage.py runserver 0.0.0.0:8010

migrate:
	pipenv run python manage.py migrate

collectstatic:
	pipenv run python manage.py collectstatic --link --noinput

graphql_schema:
	pipenv run python manage.py graphql_schema --schema config.schema.schema --out schema.json

lint:
	pipenv run isort --recursive --check-only .
	pipenv run black --check .
	pipenv run flake8 .

format:
	pipenv run isort --recursive .
	pipenv run black .

test:
	pipenv run pytest -n 4

coverage:
	pipenv run pytest --cov=klasse --cov-report term-missing
