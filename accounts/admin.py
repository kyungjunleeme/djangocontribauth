from django.contrib import admin
from .models import User, Profile
from .forms import CustomUserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    form = CustomUserForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]
