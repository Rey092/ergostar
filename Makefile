# define variables
ENV_PREFIX=.venv/bin/
PARAMS=--pythonpath=. --settings=app.unfold
UNFOLD_MODELS=src/infrastructure/unfold/models.py

run:
	litestar --app app.landing:app run -r -I *.html -I *.css -I *.js

landing:
	make run

# UNFOLD
# ------------------------------------------
unfold:
	django-admin runserver $(PARAMS) 127.0.0.1:8001

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

init:
	litestar --app app.landing:app init landing

# DEPLOY
# ------------------------------------------
gunilanding:
	gunicorn -c gunicorn_landing.py
