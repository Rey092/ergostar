# UNFOLD VARIABLES
# ------------------------------------------
MANAGE=python manage.py
UNFOLD_MODELS=admin/models.py
UNFOLD_RUN_PARAMS=--pythonpath=. --settings=admin.config.settings

# LITESTAR VARIABLES
# ------------------------------------------
LITESTAR_RUN_PARAMS=-r -I *.html -I *.css -I *.js -I *.svelte
LITESTAR_API_APP=src.main.api:create_app

# RUN COMMANDS
# ------------------------------------------
run:
	litestar run $(LITESTAR_RUN_PARAMS)

unfold:
	django-admin runserver $(UNFOLD_RUN_PARAMS) 127.0.0.1:8000

# DATABASE
# ------------------------------------------
drop:
	@echo "ATTENTION: This operation will drop all tables in the database."
	litestar core drop-db
	litestar database upgrade

seed:
	litestar core seed-db

initdb:
	litestar database init ./src/db/migrations

migrate:          ## Generate database migrations
	@echo "ATTENTION: Will apply all database migrations."
	litestar database upgrade

migrations:       ## Generate database migrations
	@echo "ATTENTION: This operation will create a new database migration for any defined models changes."
	litestar database make-migrations --autogenerate

# DATABASE UNFOLD
# ------------------------------------------

unfold-seed:
	django-admin seed $(UNFOLD_RUN_PARAMS)

unfold-migrate:
	django-admin migrate $(UNFOLD_RUN_PARAMS)

unfold-migrations:
	django-admin makemigrations $(UNFOLD_RUN_PARAMS)

unfold-generate:
	# generate a models from an existing database ('main') using django
	django-admin inspectdb $(UNFOLD_RUN_PARAMS) --database=main $(PARAMS) > $(UNFOLD_MODELS)
	# delete a first line
	sed -i '1d' $(UNFOLD_MODELS)
	# add 'Unfold' before each (models.Model)
	sed -i 's/(models.Model)/Unfold(models.Model)/g' $(UNFOLD_MODELS)

# DEPLOY
# ------------------------------------------
run-docker:
	gunicorn $(LITESTAR_API_APP) \
		--bind 0.0.0.0:8000 \
		--worker-class 'uvicorn.workers.UvicornWorker' \
		--workers 1 \
		--access-logfile '-' \
		--error-log '-' \
		--log-level 'info' \
		--forwarded-allow-ips '*' \
		--access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

unfold-docker:
	# TODO: update the command
	gunicorn admin.config.wsgi:application \
		--bind 0.0.0.0:8000 \
		--workers 1 \
		--access-logfile '-' \
		--error-log '-' \
		--log-level 'info' \
		--forwarded-allow-ips '*' \
		--access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

migrator-docker:
	litestar database upgrade --no-prompt
	litestar core seed-db
	django-admin migrate --noinput $(UNFOLD_RUN_PARAMS)
	django-admin collectstatic --noinput $(UNFOLD_RUN_PARAMS)
	django-admin seed $(UNFOLD_RUN_PARAMS)

# ETC.
# ------------------------------------------
tree:
	tree -I '*.css|__pycache__|*.js|*.svg|*.png|*.jpg|static|versions|*.html|__init__.py'

lint:
	pre-commit run --all-files
