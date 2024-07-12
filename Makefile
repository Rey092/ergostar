# define variables
ENV_PREFIX=.venv/bin/
PARAMS=--pythonpath=. --settings=src.infra.unfold.app
LITESTAR_LANDING_APP=src.infra.litestar.app_landing:app
UNFOLD_MODELS=src/infra/unfold/models.py

init:
	export LITESTAR_APP=$(LITESTAR_LANDING_APP)

landing:
	litestar --app $(LITESTAR_LANDING_APP) run -r -I *.html -I *.css -I *.js

unfold:
	django-admin runserver $(PARAMS) 127.0.0.1:8001

# UNFOLD
# ------------------------------------------

unfold-migrate:
	django-admin migrate $(PARAMS)

unfold-docker:
	gunicorn app.unfold:application

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



# DATABASE
# ------------------------------------------
initdb:
	litestar --app app.landing:app database init ./src/db/migrations

migrations:       ## Generate database migrations
	@echo "ATTENTION: This operation will create a new database migration for any defined models changes."
	@while [ -z "$$MIGRATION_MESSAGE" ]; do read -r -p "Migration message: " MIGRATION_MESSAGE; done ;
	litestar --app app.landing:app database make-migrations --autogenerate -m "$${MIGRATION_MESSAGE}"

migrate:          ## Generate database migrations
	@echo "ATTENTION: Will apply all database migrations."
	litestar --app app.landing:app database upgrade

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
