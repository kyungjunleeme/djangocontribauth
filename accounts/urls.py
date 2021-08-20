from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

# app_name = 'accounts' # 설정 시 오류 발생

urlpatterns = [
    # path("signup/", views.signup, name="signup"),
    # path("signup/", views.SignupView.as_view(), name="signup"),
    path("signup/", views.SignupNewView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/url/",
        views.RequestLoginViaUrlView.as_view(),
        name="request_login_via_url",
    ),
    path("login/<uidb64>/<token>/", views.login_via_url, name="login_via_url"),
    path(
        "password_change/", views.MyPasswordChangeView.as_view(), name="password_change"
    ),
    path("password_reset/", views.MyPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # path("", views.home, name="home"),
    #   path('password_change/done/',
    #       auth_views.PasswordChangeDoneView.as_view(
    #           template_name='accounts/password_change_done.html'
    #       ),
    #   name='password_change_done'),
]
