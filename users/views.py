from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileForm


# Create your views here.


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="users:register")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо {username}! Ваш акаунт успішно зареєстровано!")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})
