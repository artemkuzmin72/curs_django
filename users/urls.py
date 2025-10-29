from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"), 
         name="password_reset"),
    path("password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), 
         name="password_reset_complete"),
    path("stats/", views.UserStatsView.as_view(), name="user_stats"),
    path('users/', views.user_list, name='user_list'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
]