from django.urls import path
from blog import views


app_name = 'blog' # URL Reverse에서 namespace역할을 하게 됨

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]