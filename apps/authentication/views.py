from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView

from .forms import LoginForm
from django.contrib import messages

# Create your views here.


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user:
            login(self.request, user)
            return redirect('dashboard:view')

        messages.error(self.request, 'Username dan atau password salah', extra_tags='danger')
        return self.get(self.request)

    def form_invalid(self, form):
        print(form.errors)
        return self.get(self.request)
