from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import FormView

from .forms import SignUPForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from order_food.models import Wallet


class SignUpView(FormView):
    form_class = SignUPForm
    template_name = "registration/sign_up.html"

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            wallet = Wallet.objects.create(student=user, amount=0)
            wallet.save()
            login(self.request, user)
            return redirect('order_food:home')


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = reverse_lazy("order_food:home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("order_food:index")




