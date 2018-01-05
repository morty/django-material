from django.contrib.auth import views, forms
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.utils.decorators import method_decorator
from django.views import generic

from material import (
    Viewset, viewprop, Icon,
    MaterialTextInput, MaterialPasswordInput
)


class AuthenticationForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = MaterialTextInput(
            attrs={'autofocus': True},
            prefix=Icon('account_box')
        )
        self.fields['password'].widget = MaterialPasswordInput(
            prefix=Icon('lock')
        )


@method_decorator(
    user_passes_test(lambda u: u.is_authenticated),
    name='dispatch')
class ProfileView(generic.DetailView):
    template_name = 'registration/profile.html'

    def get_object(self):
        return self.request.user


class AuthViewset(Viewset):
    """
    Viewset for the `django.contrib.auth`.

    urlpatterns = [
        path('accounts/', AuthViewset(
            login_view=views.LoginView.as_view(
                authentication_form=MyAuthForm
            )
        ).urls),
    ]
    """

    def __init__(self, *, allow_password_change=True, with_profile_view=True, **kwargs):
        """
            Initialize the viewset.

            :param allow_password_change=True: enable password change/reset views
        """
        super().__init__(**kwargs)
        self.allow_password_change = allow_password_change
        self.with_profile_view = with_profile_view

    """
    Login
    """
    login_view_class = views.LoginView

    def get_login_view_kwargs(self, **kwargs):
        result = {
            'form_class': AuthenticationForm
        }
        result.update(kwargs)
        return result

    @viewprop
    def login_view(self):
        return self.login_view_class.as_view(**self.get_login_view_kwargs())

    @property
    def login_url(self):
        return path('login/', self.login_view, name='login')

    """
    Logout
    """
    logout_view_class = views.LogoutView

    def get_logout_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def logout_view(self):
        return self.logout_view_class.as_view(**self.get_logout_view_kwargs())

    @property
    def logout_url(self):
        return path('logout/', self.logout_view, name='logout')

    """
    Password Change
    """
    pass_change_view_class = views.PasswordChangeView

    def get_pass_change_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_change_view(self):
        return self.pass_change_view_class.as_view(**self.get_pass_change_view_kwargs())

    @property
    def pass_change_url(self):
        if self.allow_password_change:
            return path(
                'password_change/', self.pass_change_view,
                name='password_change')

    """
    Password Change Done
    """
    pass_change_done_view_class = views.PasswordChangeDoneView

    def get_pass_change_done_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_change_done_view(self):
        return self.pass_change_done_view_class.as_view(**self.get_pass_change_done_view_kwargs())

    @property
    def pass_change_done_url(self):
        if self.allow_password_change:
            return path(
                'password_change/done/', self.pass_change_done_view,
                name='password_change_done')

    """
    Password Reset Request
    """
    pass_reset_view_class = views.PasswordResetView

    def get_pass_reset_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_reset_view(self):
        return self.pass_reset_view_class.as_view(**self.get_pass_reset_view_kwargs())

    @property
    def pass_reset_url(self):
        if self.allow_password_change:
            return path(
                'password_reset/', self.pass_reset_view,
                name='password_reset')

    """
    Password Reset Request Done
    """
    pass_reset_done_view_class = views.PasswordResetDoneView

    def get_pass_reset_done_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_reset_done_view(self):
        return self.pass_reset_done_view_class.as_view(**self.get_pass_reset_done_view_kwargs())

    @property
    def pass_reset_done_url(self):
        if self.allow_password_change:
            return path(
                'password_reset/done/', self.pass_reset_done_view,
                name='password_reset_done')

    """
    Password Reset Request Confirm
    """
    pass_reset_confirm_view_class = views.PasswordResetConfirmView

    def get_pass_reset_confirm_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_reset_confirm_view(self):
        return self.pass_reset_confirm_view_class.as_view(**self.get_pass_reset_confirm_view_kwargs())

    @property
    def pass_reset_confirm_url(self):
        if self.allow_password_change:
            return path(
                'reset/<uidb64>/<token>/', self.pass_reset_confirm_view,
                name='password_reset_confirm')

    """
    Password Request Request Confirmed
    """
    pass_reset_complete_view_class = views.PasswordResetCompleteView

    def get_pass_reset_complete_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def pass_reset_complete_view(self):
        return self.pass_reset_complete_view_class.as_view(**self.get_pass_reset_complete_view_kwargs())

    @property
    def pass_reset_complete_url(self):
        if self.allow_password_change:
            return path(
                'reset/done/', self.pass_reset_complete_view,
                name='password_reset_complete')
    """
    Profile
    """
    profile_view_class = ProfileView

    def get_profile_view_kwargs(self, **kwargs):
        return kwargs

    @viewprop
    def profile_view(self):
        return self.profile_view_class.as_view(**self.get_profile_view_kwargs())

    @property
    def profile_url(self):
        if self.with_profile_view:
            return path('profile/', self.profile_view, name='profile')
