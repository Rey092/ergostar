
ENV_PREFIX=.venv/bin/

landing:
	litestar --app app.landing:app run -r


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
	litestar --app app.landing:app init create-all

# DEPLOY
# ------------------------------------------
gunilanding:
	gunicorn -c gunicorn_landing.py
