.PHONY: shell runserver migrate collectstatic graphql_schema lint format test coverage

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
	pipenv run isort --recursive --quiet --check-only .
	pipenv run black --check --quiet --exclude="migrations|snapshots"  .
	pipenv run flake8 .
	pipenv run bandit --recursive .

format:
	pipenv run isort --quiet --recursive .
	pipenv run black --quiet --exclude="migrations|snapshots" .

test:
	pipenv run pytest -n 4

coverage:
	pipenv run pytest --cov=klasse --cov-report term-missing
