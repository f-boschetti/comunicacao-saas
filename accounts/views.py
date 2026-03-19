"""Views for accounts app."""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, CompanyForm
from .models import Company


class CustomLoginView(LoginView):
    """Custom login view."""
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = "/"


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            company_name = form.cleaned_data["company_name"]
            slug = slugify(company_name)
            counter = 1
            original_slug = slug
            while Company.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            company = Company.objects.create(name=company_name, slug=slug)
            user.company = company
            user.role = "admin"
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Conta criada com sucesso! Bem-vindo(a)!")
            return redirect("dashboard:index")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    """User profile view."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def company_settings_view(request):
    """Company settings view."""
    company = request.user.company
    if not company:
        messages.error(request, "Você não está associado a nenhuma empresa.")
        return redirect("dashboard:index")

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados da empresa atualizados com sucesso!")
            return redirect("accounts:company_settings")
    else:
        form = CompanyForm(instance=company)

    return render(request, "accounts/company_settings.html", {"form": form, "company": company})
