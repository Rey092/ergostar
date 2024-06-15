
ENV_PREFIX=.venv/bin/

landing:
	litestar --app apps.landing:app run -r


# DATABASE
# ------------------------------------------
initdb:
	litestar --app apps.landing:app database init ./src/db/migrations

migrations:       ## Generate database migrations
	@echo "ATTENTION: This operation will create a new database migration for any defined models changes."
	@while [ -z "$$MIGRATION_MESSAGE" ]; do read -r -p "Migration message: " MIGRATION_MESSAGE; done ;
	litestar --app apps.landing:app database make-migrations --autogenerate -m "$${MIGRATION_MESSAGE}"

.PHONY: migrate
migrate:          ## Generate database migrations
	@echo "ATTENTION: Will apply all database migrations."
	litestar --app apps.landing:app database upgrade
