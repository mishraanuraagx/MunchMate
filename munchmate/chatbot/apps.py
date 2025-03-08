from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class ChatbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"

    # def ready(self):
    #     from django.contrib.auth.models import User
    #     """Creates default users when Django starts."""
    #     if not User.objects.filter(username="user1").exists():
    #         User.objects.create_user("user1", "user1@mail.com", "password123")
    #         logger.info("User "user1" created.")
    #
    #     if not User.objects.filter(username="user2").exists():
    #         User.objects.create_user("user2", "user2@mail.com", "securepass$")
    #         logger.info("User "user2" created.")
