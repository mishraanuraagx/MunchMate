from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import chatbot_view, chatbot_home, get_all_chats, simulate_conversation_view


# APIs
from .views import all_chats, chat_form, simulate_conversation

urlpatterns = [
    path("ask/", login_required(chat_form), name="chat_form"),
    path("chats/", all_chats, name="all_chats"),
    path("simulate/", login_required(simulate_conversation_view), name="simulate_conversation_view"),

    path("", login_required(chatbot_home), name="chatbot_home"),
    path("api/chats", get_all_chats, name="get_all_chats"),
    path("api/ask/", login_required(chatbot_view), name="chatbot_view"),
    path("api/simulate/", login_required(simulate_conversation), name="simulate_conversation"),
]