# UNFOLD VARIABLES
# ------------------------------------------
MANAGE=python manage.py
UNFOLD_MODELS=admin/models.py
UNFOLD_RUN_PARAMS=--pythonpath=. --settings=admin.config.settings

# LITESTAR VARIABLES
# ------------------------------------------
LITESTAR_RUN_PARAMS=-r -I *.html -I *.css -I *.js -I *.svelte
LITESTAR_DASHBOARD_APP=src.apps.dashboard:app

# RUN COMMANDS
# ------------------------------------------
run:
	litestar run $(LITESTAR_RUN_PARAMS)

unfold-run:
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
	@while [ -z "$$MIGRATION_MESSAGE" ]; do read -r -p "Migration message: " MIGRATION_MESSAGE; done ;
	litestar database make-migrations --autogenerate -m "$${MIGRATION_MESSAGE}"

# UNFOLD
# ------------------------------------------

unfold-seed:
	$(MANAGE) seed

unfold-migrate:
	$(MANAGE) migrate $(PARAMS)

unfold-generate:
	# generate a models from an existing database ('main') using django
	$(MANAGE) inspectdb --database=main $(PARAMS) > $(UNFOLD_MODELS)
	# delete a first line
	sed -i '1d' $(UNFOLD_MODELS)
	# add 'Unfold' before each (models.Model)
	sed -i 's/(models.Model)/Unfold(models.Model)/g' $(UNFOLD_MODELS)

# DEPLOY
# ------------------------------------------
dashboard-docker:
	gunicorn $(LITESTAR_DASHBOARD_APP) \
		--bind 0.0.0.0:8000 \
		--worker-class 'uvicorn.workers.UvicornWorker' \
		--workers 4 \
		--access-logfile '-' \
		--error-log '-' \
		--log-level 'info' \
		--forwarded-allow-ips '*' \
		--access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

unfold-docker:
	# TODO: update the command
	gunicorn app.unfold:app

# ETC.
# ------------------------------------------
tree:
	tree -I '*.css|__pycache__|*.js|*.svg|*.png|*.jpg|static|versions|*.html|__init__.py'

lint:
	pre-commit run --all-files
