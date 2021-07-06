from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView, \
    PasswordResetView as BasePasswordResetView, \
    PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordResetDoneView as BasePasswordResetDoneView
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.accounts.forms import RegistrationForm, AuthenticationForm, PasswordChangeForm, ProfileEditForm, PasswordResetForm, NewPasswordForm
from apps.accounts.models import User
from apps.accounts.utils.mixins import PersonalAreaMixin, MenuItem
from apps.cars.models import CarFilter
from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.car_filter import get_car_filter


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home:index')
    page_title = 'Регистрация'

    def form_valid(self, form):
        user = User.objects.create_user(**form.cleaned_data)
        login(self.request, user, backend='apps.accounts.backends.CaseInsensitiveModelBackend')
        if 'next' in self.request.POST:
            self.success_url = self.request.POST.get('next')
        return super().form_valid(form)


class LoginView(BaseLoginView, PageTitleMixin):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm

    viewname = 'accounts:login'
    page_title = 'Вход'

    def form_valid(self, form):
        response = super().form_valid(form)
        car_filter: CarFilter = get_car_filter(self.request)
        if car_filter is not None and isinstance(self.request.user, User):
            CarFilter.objects.filter(id=car_filter.id).update(user_id=self.request.user.id)
        return response


class PasswordResetView(BasePasswordResetView, PageTitleMixin):
    template_name = 'accounts/password_reset/reset_password.html'
    success_url = reverse_lazy('accounts:password:done')
    form_class = PasswordResetForm
    subject_template_name = 'emails/password_reset/reset-link-subject.html'
    email_template_name = 'emails/password_reset/reset-link.html'
    html_email_template_name = 'emails/password_reset/html-reset-link.html'

    initial_breadcrumbs = [reverse_bc(LoginView)]
    viewname = 'accounts:password:reset'
    page_title = 'Сброс пароля'


class PasswordResetDoneView(BasePasswordResetDoneView, PageTitleMixin):
    template_name = 'accounts/password_reset/reset_done.html'

    initial_breadcrumbs = [reverse_bc(LoginView)]
    page_title = PasswordResetView.page_title


class PasswordResetConfirmView(BasePasswordResetConfirmView, PageTitleMixin):
    template_name = 'accounts/password_reset/reset_password.html'
    success_url = reverse_lazy('accounts:login')
    form_class = NewPasswordForm

    initial_breadcrumbs = [reverse_bc(LoginView), reverse_bc(PasswordResetView)]
    page_title = 'Новый пароль'


# ####### PERSONAL AREA #########


@method_decorator(login_required, name='dispatch')
class PersonalAreaIndex(TemplateView, PersonalAreaMixin):
    menu = MenuItem.INDEX
    template_name = 'accounts/personal_area/index.html'


@method_decorator(login_required, name='dispatch')
class PersonalAreaGarage(View, PersonalAreaMixin):
    menu = MenuItem.GARAGE
    template_name = 'accounts/personal_area/garage.html'
    extra_breadcrumbs = Breadcrumb('Гараж', reverse_lazy('accounts:pa:garage'))

    def get(self, request, id=None):
        if id:
            self.remove_from_garage(id)

        context = {
            'car_filters': CarFilter.objects.filter(user=request.user),
        }

        return render(request, self.template_name, self.get_context_data(**context))

    def remove_from_garage(self, id):
        carfilter = CarFilter.objects.filter(id=id, user=self.request.user)
        if carfilter.exists():
            carfilter.delete()
            messages.success(self.request, f'Автомобиль {carfilter} был успешно удалён ✔', extra_tags='text-success')


@method_decorator(login_required, name='dispatch')
class PersonalAreaEdit(View, PersonalAreaMixin):
    """
        Provides both forms for profile editing and password changing.
        POST data handled by other views
    """

    menu = MenuItem.PERSONAL_DATA
    template_name = 'accounts/personal_area/edit.html'
    extra_breadcrumbs = Breadcrumb('Редактировать профиль', reverse_lazy('accounts:pa:edit'))

    def get(self, request: HttpRequest):
        context = {
            'profile_form': ProfileEditForm(instance=request.user),
            'password_form': PasswordChangeForm(user=request.user),
        }

        return render(request, self.template_name, self.get_context_data(**context))

    def post(self, request: HttpRequest):
        action = request.POST.get('action')
        if not action:
            raise Http404('No action field')

        successfully_changed = False

        if action == ProfileEditForm.ACTION_NAME:
            profile_form = ProfileEditForm(instance=request.user, data=request.POST)
            password_form = PasswordChangeForm(user=request.user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Данные были обновлены ✔', extra_tags='edit-profile text-success')
                return redirect('accounts:pa:edit')  # Redirect to the same view to prevent multiple form submitting on reload

        elif action == PasswordChangeForm.ACTION_NAME:
            profile_form = ProfileEditForm(instance=request.user, data=request.POST)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль был успешно изменён ✔', extra_tags='change-password text-success')
                return redirect('accounts:pa:edit')  # Redirect to the same view to prevent multiple form submitting on reload
        else:
            raise Http404('Could not resolve action type')

        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'successfully_changed': successfully_changed,
        }

        return render(request, self.template_name, self.get_context_data(**context))
