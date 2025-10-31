from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Mailing, MailingAttempt
from .forms import MailingForm
from .utils import send_mailing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# Пример просмотра рассылки с проверкой роли
@login_required
def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.author != request.user and request.user.role != 'manager':
        return HttpResponseForbidden("Вы не можете просматривать эту рассылку.")
    return render(request, 'mailings/mailing_detail.html', {'mailing': mailing})


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Mailing.objects.all()  # менеджер видит все
        return Mailing.objects.filter(author=user)  # обычный пользователь видит только свои

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_create.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailings/mailing_attempt_list.html"
    context_object_name = "attempts"

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    result = send_mailing(mailing)
    messages.success(request, result)
    return redirect("mailing_list")