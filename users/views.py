import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser
from .services import CustomUserService


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("mailing:home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:home")


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Email confirmation",
            message=f"Hi! Please follow the link to confirm your email {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = "edit_profile.html"

    def get_success_url(self):
        return reverse_lazy("users:user-profile", kwargs={"pk": self.object.pk})


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "users.view_customuser"
    model = CustomUser
    template_name = "all_users.html"
    context_object_name = "users"
    queryset = CustomUserService.get_all_users().order_by("id")


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = "user_profile"


class ChangeUserStatusView(PermissionRequiredMixin, View):
    permission_required = "users.can_block_user"

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        if user == request.user:
            messages.warning(request, "You cannot block yourself.")
            return redirect("users:all-users")
        user.is_active = not user.is_active
        user.save()
        return redirect("users:all-users")
