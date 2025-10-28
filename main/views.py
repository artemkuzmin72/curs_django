from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .utils import send_mailing
from .models import Recipient, Message, Mailing, MailingAttempt
from .forms import RecipientForm, MessageForm, MailingForm, RegisterForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()
# Пример просмотра рассылки с проверкой роли
@login_required
def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.author != request.user and request.user.role != 'manager':
        return HttpResponseForbidden("Вы не можете просматривать эту рассылку.")
    return render(request, 'main/mailing_detail.html', {'mailing': mailing})

# Просмотр списка всех пользователей (только менеджер)
@login_required
def user_list(request):
    if request.user.role != 'manager':
        return HttpResponseForbidden("Доступ запрещён")
    users = User.objects.all()
    return render(request, 'main/user_list.html', {'users': users})

# Блокировка пользователя (только менеджер)
@login_required
def block_user(request, user_id):
    if request.user.role != 'manager':
        return HttpResponseForbidden("Доступ запрещён")
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')
@method_decorator(cache_page(60 * 15), name='dispatch')
class HomePageView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Recipient.objects.count()
        return context

class RecipientListView(ListView):
    model = Recipient
    template_name = "main/recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "main/recipient_form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "main/recipient_form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "main/recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")

class MessageListView(ListView):
    model = Message
    template_name = "main/message_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "main/message_form.html"
    success_url = reverse_lazy("message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "main/message_form.html"
    success_url = reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "main/message_confirm_delete.html"
    success_url = reverse_lazy("message_list")

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Mailing.objects.all()  # менеджер видит все
        return Mailing.objects.filter(author=user)  # обычный пользователь видит только свои


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "main/mailing_form.html"
    success_url = reverse_lazy("mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "main/mailing_form.html"
    success_url = reverse_lazy("mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "main/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing_list")

class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "main/mailing_attempt_list.html"
    context_object_name = "attempts"

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "main/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        # Здесь можно отправить email для подтверждения регистрации
        # например через send_mail с уникальным токеном
        return super().form_valid(form)
    
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

        # Количество отправленных сообщений
        context['total_sent'] = attempts.filter(status='Успешно').count()

        return context

def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    result = send_mailing(mailing)
    messages.success(request, result)
    return redirect("mailing_list")
