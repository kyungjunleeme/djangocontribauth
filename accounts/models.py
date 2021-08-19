from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     people_type = models.CharField(
#         max_length=3,
#         choices=(
#             ("in", "employees"),
#             ("out", "outsiders"),
#         ),
#     )


class PeopleTypeChoices(models.TextChoices):
    outsider = (
        "out",
        "Outsider",
    )  # , 1)실제 db에 저장되는 값 , 2)국제화 기능에 활용할 경우 _('Freshman'), 노출되는 값
    inhandplus = "in", "Employee"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True, max_length=150)
    people_type = models.CharField(
        max_length=20, choices=PeopleTypeChoices.choices, null=True, blank=True
    )
    REQUIRED_FIELDS = ["people_type", "username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
