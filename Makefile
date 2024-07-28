# UNFOLD VARIABLES
# ------------------------------------------
UNFOLD_MODELS=config/models.py
UNFOLD_RUN_PARAMS=--pythonpath=. --settings=src.infra.unfold.app

# LITESTAR VARIABLES
# ------------------------------------------
LITESTAR_RUN_PARAMS=-r -I *.html -I *.css -I *.js -I *.svelte

# RUN COMMANDS
# ------------------------------------------
landing:
	litestar run $(LITESTAR_RUN_PARAMS)

unfold:
	django-admin runserver $(UNFOLD_RUN_PARAMS) 127.0.0.1:8001

# DATABASE
# ------------------------------------------
drop:
	@echo "ATTENTION: This operation will drop all tables in the database."
	litestar seed drop
	litestar database upgrade

seed:
	litestar seed data

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

unfold-migrate:
	django-admin migrate $(PARAMS)

unfold-docker:
	gunicorn app.unfold:app

unfold-generate:
	# generate a models from an existing database ('main') using django
	django-admin inspectdb --database=main $(PARAMS) > $(UNFOLD_MODELS)
	# delete a first line
	sed -i '1d' $(UNFOLD_MODELS)
	# Add 'app_label = '__main__'' undear each 'class Meta:' in models.py
	sed -i '/class Meta:/a \ \ \ \     app_label = "__main__"' $(UNFOLD_MODELS)
	# if CharField( without 'max' after '(' found, add "max_length=255, " after CharField(
	sed -i "/CharField(/ {/max/! s/CharField(/CharField(max_length=255, /}" $(UNFOLD_MODELS)
	# add 'Unfold' before each (models.Model)
	sed -i 's/(models.Model)/Unfold(models.Model)/g' $(UNFOLD_MODELS)

# DEPLOY
# ------------------------------------------
landing-docker:
	#gunicorn -c gunicorn_landing.py
	gunicorn $(LITESTAR_LANDING_APP) \
		--bind 0.0.0.0:8000 \
		--worker-class 'uvicorn.workers.UvicornWorker' \
		--workers 4 \
		--access-logfile '-' \
		--error-log '-' \
		--log-level 'info' \
		--forwarded-allow-ips '*' \
		--access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# ETC.
# ------------------------------------------
tree:
	tree -I '*.css|__pycache__|*.js|*.svg|*.png|*.jpg|static|versions|*.html|__init__.py'

lint:
	pre-commit run --all-files
