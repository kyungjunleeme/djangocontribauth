from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render, resolve_url
from django.views.generic import CreateView
from accounts.forms import CustomUserForm
from django.contrib.auth import get_user_model

User = get_user_model()  # "accounts.User" 사용함


@login_required  # Logout 상황이면 -> settings.LOGIN_URL 로 이동해준다. 그건 ?next=뒤에 인자값으로 확인 가능
def profile(request):
    # https://github.com/django/django/blob/main/django/contrib/auth/models.py 내 User , AnonymousUser 모델 클래스는 아니고 단순 클래스
    # request.user # https://github.com/django/django/blob/main/django/contrib/auth/context_processors.py
    return render(request, "accounts/profile.html")


# 로그인 처리 참고
# https://github.com/django/django/blob/main/django/contrib/auth/views.py
# def form_valid(self, form):
#     """Security check complete. Log the user in."""
#     auth_login(self.request, form.get_user())
#     return HttpResponseRedirect(self.get_success_url())


# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # 회원 가입 완료 및 user 모델의 객체 생성
#             auth_login(request, user)  # 로그인 처리
#             next_url = request.GET.get("next") or "profile"
#             # <QueryDict: {'next': ['이동할 주소']}>
#             # cf) 밑의 표현이랑 다름 "next"
#             # request.GET은 QueryDict 객체(동일한 키값으로 여러개 value를 가질 수 있음)
#             # get() 메서드는 키값이 딕셔너리 안에 있으면 밸류값을 리턴해준다. 키값이 존재하지 않으면 디폴트값 None을 리턴한다.
#             # https://github.com/django/django/blob/main/django/http/request.py#L54
#             return redirect(next_url)
#             # return redirect(settings.LOGIN_URL)
#     else:
#         form = SignupForm()
#     return render(
#         request,
#         "accounts/signup.html",
#         {
#             "form": form,
#         },
#     )


# class SignupView(CreateView):
#     model = User
#     form_class = SignupForm
#     template_name = "accounts/signup.html"
#     # success_url = reverse_lazy("profile") # 경준 추가

#     def get_success_url(self):
#         next_url = self.request.GET.get("next") or "profile"
#         # 여기서 "profile"은 실제 URL 문자열이 아니지만 resolve_url 내부에서 이를 처리해 준다
#         # 그래서 Reverse("profile") 이런 처리를 해줄 필요가 없다. 또한 redirect도 마찬가지다
#         # 또한 redirect은 내부적으로 resovle_url을 사용한다.
#         return resolve_url(next_url)
#         # return resolve_url("profile")

#     # def get_success_url(self) -> str:
#     #     return resolve_url('profile')
#     # cf) 추가 공부 필요
#     # https://stackoverflow.com/questions/42397502/how-to-use-python-type-hints-with-django-queryset
#     # def form_valid(self, form: _ModelFormT) -> HttpResponse:
#     #     return super().form_valid(form)

#     def form_valid(self, form):
#         user = form.save()
#         auth_login(self.request, user)
#         return redirect(self.get_success_url())


# signup = SignupView.as_view()

# RequestLoginViaUrlView 이 self
class RequestLoginViaUrlView(PasswordResetView):
    # form_class = TestForm
    template_name = "accounts/request_login_via_url_form.html"
    subject_template_name = (
        "accounts/login_auth_subject.txt"  # registration/password_reset_subject.txt
    )
    email_template_name = "accounts/login_via_url.html"
    success_url = settings.LOGIN_URL
    # Note: may have been skipped because of "justMyCode" option (default == true). Try setting "justMyCode": false in the debug configuration (e.g., launch.json).


# request_login_via_url = RequestLoginViaUrlView.as_view()


def login_via_url(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        raise Http404

    if default_token_generator.check_token(current_user, token):
        auth_login(request, current_user)
        messages.info(request, "로그인이 승인되었습니다.")
        return redirect("root")

    messages.error(request, "로그인이 거부되었습니다.")
    return redirect("root")


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("profile")
    template_name = "accounts/password_change_form.html"

    def form_valid(self, form):
        messages.info(self.request, "암호 변경을 완료했습니다.")
        return super().form_valid(form)


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("login")
    template_name = "accounts/password_reset_form.html"
    # email_template_name = ...
    # html_email_template_name = ...

    def form_valid(self, form):
        messages.info(self.request, "암호 변경 메일을 발송했습니다.")
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("login")
    template_name = "accounts/password_reset_confirm.html"

    def form_valid(self, form):
        messages.info(self.request, "암호 리셋을 완료했습니다.")
        return super().form_valid(form)


def home(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponse("User was created successfully.")
        else:
            return HttpResponse("There was an error.")
    else:
        form = CustomUserForm()
    return render(request, "accounts/home.html", {"form": form})
