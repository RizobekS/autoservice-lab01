from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView, \
    PasswordResetView as BasePasswordResetView, \
    PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordResetDoneView as BasePasswordResetDoneView, redirect_to_login
from django.http import HttpRequest, Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView, ListView

from apps.accounts.forms import RegistrationForm, AuthenticationForm, PasswordChangeForm, ProfileEditForm, PasswordResetForm, NewPasswordForm, AppointmentForm
from apps.accounts.models import User, Appointment
from apps.accounts.utils.mixins import PersonalAreaMixin
from apps.cars.models import CarFilter
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.car_filter import get_car_filter, remove_car_filter
from utils.mixins import PageSettingsMixin


class RegisterView(FormView, PageSettingsMixin):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home:index')

    viewname = 'accounts:register'

    def form_valid(self, form):
        user = User.objects.create_user(**form.cleaned_data)
        login(self.request, user, backend='apps.accounts.backends.CaseInsensitiveModelBackend')
        if 'next' in self.request.POST:
            self.success_url = self.request.POST.get('next')
        return super().form_valid(form)


class LoginView(BaseLoginView, PageSettingsMixin):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm

    viewname = 'accounts:login'

    def form_valid(self, form):
        response = super().form_valid(form)
        car_filter: CarFilter = get_car_filter(self.request)
        if car_filter is not None and isinstance(self.request.user, User):
            CarFilter.objects.filter(id=car_filter.id).update(user_id=self.request.user.id)
        return response


class PasswordResetView(BasePasswordResetView, PageSettingsMixin):
    template_name = 'accounts/password_reset/reset_password.html'
    success_url = reverse_lazy('accounts:password:done')
    form_class = PasswordResetForm
    subject_template_name = 'accounts/emails/password_reset/reset-link-subject.html'
    email_template_name = 'accounts/emails/password_reset/reset-link.html'
    html_email_template_name = 'accounts/emails/password_reset/html-reset-link.html'

    initial_breadcrumbs = [reverse_bc(LoginView)]
    viewname = 'accounts:password:reset'


class PasswordResetDoneView(BasePasswordResetDoneView, PageSettingsMixin):
    template_name = 'accounts/password_reset/reset_done.html'

    initial_breadcrumbs = [reverse_bc(LoginView)]
    viewname = 'accounts:password:done'


class PasswordResetConfirmView(BasePasswordResetConfirmView, PageSettingsMixin):
    template_name = 'accounts/password_reset/reset_password.html'
    success_url = reverse_lazy('accounts:login')
    form_class = NewPasswordForm

    initial_breadcrumbs = [reverse_bc(LoginView), reverse_bc(PasswordResetView)]
    viewname = 'accounts:password:new-password'

    def form_valid(self, form):
        messages.success(self.request, '✔ Новый пароль успешно создан!<br/>Войдите в аккаунт с новым паролем.', extra_tags='text-success')
        return super().form_valid(form)


class SubmitAppointmentView(View):

    def post(self, request):
        if not request.is_ajax():
            raise Http404()

        data = self.request.POST.copy()
        data['user'] = self.request.user.id if self.request.user.is_authenticated else None
        form = AppointmentForm(data=data)
        if form.is_valid():
            form.send_mail(request)
            form.save()

            # Initial data for the form
            if request.user.is_authenticated and request.user.carfilter_set.exists():
                car = request.user.carfilter_set.select_related('vendor', 'model__vendor', 'year__model__vendor', 'modification__year__model__vendor').latest()
            else:
                car = get_car_filter(request)

            initial = {
                'full_name': request.user.get_full_name() if request.user.is_authenticated else '',
                'car': car.full_name() if car else '',
            }

            response = {'success': True, **initial}
        else:
            response = {'success': False, **form.errors}

        return JsonResponse(response)


# ####### PERSONAL AREA #########


@method_decorator(login_required, name='dispatch')
class PersonalAreaIndex(TemplateView, PersonalAreaMixin):
    template_name = 'accounts/personal_area/index.html'

    def get_current_breadcrumb(self):
        return []


@method_decorator(login_required, name='dispatch')
class AppointmentListView(ListView, PersonalAreaMixin):
    template_name = 'accounts/personal_area/appointment_list.html'
    current_breadcrumb = Breadcrumb('Записи на сервис', reverse_lazy('accounts:pa:appointment:list'))

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class PersonalAreaGarage(View, PersonalAreaMixin):
    template_name = 'accounts/personal_area/garage.html'
    current_breadcrumb = Breadcrumb('Гараж', reverse_lazy('accounts:pa:garage'))

    def get(self, request, id=None):
        if id:
            return self.remove_from_garage(request, id)

        redirect_to_login(reverse('accounts:pa:garage'))
        context = {
            'car_filters': CarFilter.objects.filter(user=request.user),
        }

        return render(request, self.template_name, self.get_context_data(**context))

    def remove_from_garage(self, request, id):
        if self.request.user.is_authenticated:
            carfilter = CarFilter.objects.filter(id=id, user=self.request.user)
            if carfilter.exists():
                carfilter.delete()
                messages.success(self.request, f'Автомобиль {carfilter} был успешно удалён ✔', extra_tags='text-success')
            return self.get(request)  # call get() again, but without id (because it is already removed)
        else:  # For not authenticated user
            remove_car_filter(self.request)
            return HttpResponse(status=200)


@method_decorator(login_required, name='dispatch')
class PersonalAreaEdit(View, PersonalAreaMixin):
    """
        Provides both forms for profile editing and password changing.
        POST data handled by other views
    """
    template_name = 'accounts/personal_area/edit.html'
    current_breadcrumb = Breadcrumb('Редактировать профиль', reverse_lazy('accounts:pa:edit'))

    def get(self, request: HttpRequest):
        context = {
            'profile_form': ProfileEditForm(instance=request.user),
            'password_form': PasswordChangeForm(user=request.user),
        }

        return render(request, self.template_name, self.get_context_data(**context))

    def post(self, request):
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
