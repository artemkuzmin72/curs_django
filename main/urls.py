from django.urls import path
from .views import (
    HomePageView, RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
)

urlpatterns = [
    # Главная
    path("", HomePageView.as_view(), name="home"),

    # Получатели
    path("clients/", RecipientListView.as_view(), name="recipient_list"),
    path("clients/add/", RecipientCreateView.as_view(), name="recipient_create"),
    path("clients/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("clients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/add/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]
