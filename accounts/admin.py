from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import User, Profile
from .forms import CustomUserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # pass
    # model = User
    form = CustomUserForm


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["user", "bio"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [profile.name for profile in Profile._meta.fields]
    # list_select_related = ['user']

    # def get_queryset(self, request: HttpRequest) -> QuerySet:
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related("user")
