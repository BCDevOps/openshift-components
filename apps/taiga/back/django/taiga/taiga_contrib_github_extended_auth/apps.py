import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class TaigaGithubExtendedAuthAppConfig(AppConfig):
    name = "taiga.taiga_contrib_github_extended_auth"
    verbose_name = "Taiga contrib github extended auth App Config"

    def ready(self):
        from taiga.auth.services import register_auth_plugin
        from . import services
        logger.debug("Registering taiga_contrib_github_extended_auth.")
        register_auth_plugin("github", services.github_login_func)
