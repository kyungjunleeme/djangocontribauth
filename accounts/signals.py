from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_post_save_for_user(sender, **kwargs):
    if kwargs["created"]:
        # 가입시기
        user = kwargs["instance"]
        Profile.objects.create(user=user)

        # 환영 이메일
