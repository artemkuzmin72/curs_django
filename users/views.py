from django.views.generic import TemplateView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from users.models import CustomUser
from mailings.models import MailingAttempt
from .forms import RegisterForm

User = get_user_model()


# Просмотр списка всех пользователей (только менеджер)
@login_required
def user_list(request):
    if request.user.role != 'manager':
        return HttpResponseForbidden("Доступ запрещён")
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


# Блокировка / разблокировка пользователя (только менеджер)
@user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')
def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"Пользователь {user.email} {'разблокирован' if user.is_active else 'заблокирован'}.")
    return redirect('users:user_list')


# Кэширование страницы статистики на 15 минут
@method_decorator(cache_page(60 * 15), name='dispatch')
class UserStatsView(TemplateView):
    template_name = "main/user_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Количество успешных и неуспешных попыток
        attempts = MailingAttempt.objects.filter(mailing__author=user)
        context['success_count'] = attempts.filter(status='Успешно').count()
        context['failed_count'] = attempts.filter(status='Не успешно').count()
        context['total_sent'] = attempts.count()

        return context


# Регистрация нового пользователя
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True  # теперь пользователь активен и может войти
        user.save()
        return super().form_valid(form)