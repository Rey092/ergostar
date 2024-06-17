"""Server plugins."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.plugins.structlog import StructlogPlugin
from sqladmin_litestar_plugin import SQLAdminPlugin

from config import plugins as config
from config import settings

# from litestar_granian import GranianPlugin
# from litestar_saq import SAQPlugin
from server.builder import ApplicationConfigurator
from src.sql_admin import sql_admin_views

structlog = StructlogPlugin(config=config.log)
# saq = SAQPlugin(config=config.saq)
alchemy = SQLAlchemyPlugin(config=config.alchemy)
# granian = GranianPlugin()
app_config = ApplicationConfigurator()
admin = SQLAdminPlugin(
    views=sql_admin_views, engine=settings.db.engine, base_url="/admin/"
)
