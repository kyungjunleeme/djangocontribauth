from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required # Logout 상황이면 -> settings.LOGIN_URL 로 이동해준다. 그건 ?next=뒤에 인자값으로 확인 가능
def profile(request):
    # https://github.com/django/django/blob/main/django/contrib/auth/models.py 내 User , AnonymousUser 모델 클래스는 아니고 단순 클래스
    # request.user # https://github.com/django/django/blob/main/django/contrib/auth/context_processors.py
    return render(request, 'accounts/profile.html')
