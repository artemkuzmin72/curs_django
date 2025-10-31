from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Recipient, Message
from mailings.models import Mailing
from .forms import RecipientForm, MessageForm
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()

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

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Recipient.objects.all()  # менеджер видит все
        return Recipient.objects.filter(author=user) 


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "main/recipient_form.html"
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "main/recipient_form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "main/recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'recipients/recipient_detail.html'

class MessageListView(ListView):
    model = Message
    template_name = "main/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'manager':
            return Message.objects.all()
        return Message.objects.filter(author=user)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "main/message_form.html"
    success_url = reverse_lazy("message_list")

    def form_valid(self, form):
        # Автоматически присваиваем текущего пользователя
        form.instance.author = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "main/message_form.html"
    success_url = reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "main/message_confirm_delete.html"
    success_url = reverse_lazy("message_list")

class MessageDetailView(DetailView):
    model = Message
    template_name = 'messages/message_detail.html'
