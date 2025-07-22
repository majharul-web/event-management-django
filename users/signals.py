from django.db.models.signals import post_save,pre_save,pre_delete,post_delete,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # make token
        token=default_token_generator.make_token(instance)
        activation_link=f"{settings.FRONTEND_URL}/users/activate/{instance.pk}/{token}/"
        
        try:
            send_mail(
                subject="Welcome to Event Manager",
                message=f"Hello {instance.username},\n\nThank you for joining our platform!\n\nPlease activate your account by clicking the link below:\n{activation_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False
            )

        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        # Assign default role to the user
        user_group,created = Group.objects.get_or_create(name='Participant')
        if user_group:
            instance.groups.add(user_group)
            instance.save()
