from django.urls import path
from . import views
from .views import send_mailing_view

app_name = 'mailings'

urlpatterns = [
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path("create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/edit/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/send/", views.send_mailing_view, name="mailing_send"),
    path("attempts/", views.MailingAttemptListView.as_view(), name="mailing_attempt_list"),
    path("<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
]