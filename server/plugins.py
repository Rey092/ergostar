"""Server plugins."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from config import plugins as config
from litestar.plugins.structlog import StructlogPlugin
# from litestar_granian import GranianPlugin
# from litestar_saq import SAQPlugin

# from app.config import app as config
from server.builder import ApplicationConfigurator

structlog = StructlogPlugin(config=config.log)
# vite = VitePlugin(config=config.vite)
# saq = SAQPlugin(config=config.saq)
alchemy = SQLAlchemyPlugin(config=config.alchemy)
# granian = GranianPlugin()
app_config = ApplicationConfigurator()
