from django.views.generic import ListView, DetailView, UpdateView, View
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib import messages

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
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Поздравляем с регистрацией!"
        message = """Примите наши поздравления с регистрацией в нашем сервисе!
        Теперь вы можете просматривать продукты и управлять ими"""
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "edit_profile.html"
    fields = ["country", "phone_number", "avatar"]

    def get_success_url(self):
        return reverse_lazy("users:user-profile", kwargs={"pk": self.object.pk})


class UsersListView(PermissionRequiredMixin, ListView):
    permission_required = "users.view_user"
    model = CustomUser
    template_name = "all_users.html"
    context_object_name = "users"
    queryset = CustomUser.objects.all().order_by("id")


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




