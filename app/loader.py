import importlib
import pkgutil
import logging

LOGGER = logging.getLogger(__name__)

async def load_plugins(app):
    import app.plugins as plugins_package

    for module_info in pkgutil.iter_modules(plugins_package.__path__):
        module_name = module_info.name

        if module_name.startswith("_"):
            continue

        try:
            module = importlib.import_module(f"app.plugins.{module_name}")

            if hasattr(module, "register"):
                await module.register(app)

            LOGGER.info(f"Loaded plugin: {module_name}")

        except Exception as e:
            LOGGER.error(f"Failed to load plugin {module_name}: {e}")
