from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .forms import RegistrationForm
from django.contrib import messages
from django.views import View
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm




class UserRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_singup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"https://tutormediabd.onrender.com/accounts/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return redirect('login')


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('signup')


class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    # def form_valid(self, form):
    #     messages.success(self.request, "Login successfully. Welcome Back!")
    #     return super().form_valid(form)

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('homepage')
    

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})

@login_required
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user) # password update korbe
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'pass_change.html', {'form':form})
    else:
        return redirect('login')
    
