from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounting.forms import LoginForm, ProfileForm, CustomPasswordChangeForm, DocumentTemplateForm
from accounting.models import DocumentTemplate


def page_not_found(request, exception):
    return render(request, 'accounting/404.html', {}, status=404)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Uğurla daxil oldunuz!')
                return redirect('student:student_list')
            else:
                messages.error(request, f"Xəta: İstifadəçi adı və ya şifrə yalışdır! Məlumatları bir daha yoxlayın.")
    else:
        form = LoginForm()
    return render(request, 'accounting/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounting:login')


@login_required
def profile_update(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profil uğurla yeniləndi!')
            return redirect('accounting:profile_update')
    else:
        profile_form = ProfileForm(instance=request.user)

    return render(request, 'accounting/profile.html', {
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Обновляем сессию пользователя
            messages.success(request, 'Şifrə uğurla dəyişdirildi!')
            return redirect('accounting:change_password')
    else:
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'accounting/change_password.html', {
        'password_form': password_form,
    })


class ContractListView(LoginRequiredMixin, ListView):
    model = DocumentTemplate
    context_object_name = 'templates'
    template_name = 'accounting/contract_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UploadContractView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DocumentTemplate
    form_class = DocumentTemplateForm
    template_name = 'accounting/upload_contract.html'
    success_url = reverse_lazy('accounting:contract_list')
    success_message = 'Müqavilə uğurla yükləndi'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class DeleteContractView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DocumentTemplate
    template_name = 'accounting/delete_confirm_contract.html'
    success_url = reverse_lazy('accounting:contract_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context
