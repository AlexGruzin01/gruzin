from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from myblog.models import Post
from mysite import settings


# https://www.youtube.com/watch?v=9gzJAS5e_FY
User = get_user_model()
@receiver(post_save, sender=User)
def user_save(sender, instance, created, **kwargs):
    if created:
        subject = instance.first_name + " " + instance.last_name
        message = f"Hello {instance.first_name} {instance.last_name}!"
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])