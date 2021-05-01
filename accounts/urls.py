from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import signup, activate, activation_sent, activation_not_sent
from .forms import UserLoginForm, PasswordReset, PasswordChange

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', signup, name='signup'),

    path('change_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=PasswordChange, success_url=reverse_lazy('reset_complete'),
                                                                                          template_name='registration/password_change.html'), name='password_reset'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('activation_unsuccessful/', activation_not_sent, name='activation_unsuccessful'),

    re_path(r'^account_activation_sent/$', activation_sent, name='activation_sent'),

    path('reset_password/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('reset_done'),
                                                                 form_class=PasswordReset,
                                                                 subject_template_name='registration/email_subject.txt',
                                                                 email_template_name='registration'
                                                                                     '/password_reset_email_text.html',
                                                                 html_email_template_name='registration'
                                                                                          '/password_reset_email.html'),
         name='reset'),

    path('reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_confirm'
                                                                               '.html'), name='reset_done'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('login')), name='password_change')
]
