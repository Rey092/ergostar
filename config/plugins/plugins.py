"""Server plugins."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.plugins.structlog import StructlogPlugin
# from litestar_saq import SAQPlugin

from config.plugins.builder import ApplicationConfigurator
from config.plugins import configs as config
# from src.infra import settings

structlog = StructlogPlugin(config=config.log)
# saq = SAQPlugin(config=config.saq)
alchemy = SQLAlchemyPlugin(config=config.alchemy)
app_config = ApplicationConfigurator()
