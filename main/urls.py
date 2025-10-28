from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView, RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingAttemptListView, RegisterView, UserStatsView, mailing_detail, block_user, user_list
)
from .views import send_mailing_view

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

    # Рассылки
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/add/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/<int:pk>/send/", send_mailing_view, name="mailing_send"),
    path("attempts/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),

    # Регистрация
    path("register/", RegisterView.as_view(), name="register"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Восстановление пароля
    path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="main/password_reset_form.html"), 
         name="password_reset"),
    path("password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="main/password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="main/password_reset_complete.html"), 
         name="password_reset_complete"),

    path("stats/", UserStatsView.as_view(), name="user_stats"),

    path('users/', user_list, name='user_list'),
    path('users/block/<int:user_id>/', block_user, name='block_user'),
    path('mailings/<int:pk>/', mailing_detail, name='mailing_detail'),
]
