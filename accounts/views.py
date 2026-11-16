
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterForm


class RegisterView(CreateView):

    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):

        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class UserLoginView(LoginView):

    template_name = 'accounts/login.html'

    redirect_authenticated_user = True


class UserLogoutView(LogoutView):

    next_page = 'login'


@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )
