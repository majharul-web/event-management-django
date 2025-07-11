from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event

@receiver(m2m_changed, sender=Event.rsvps.through)
def send_rsvp_confirmation_email(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = instance.rsvps.model.objects.get(pk=user_id)
            send_mail(
                subject="RSVP Confirmation - Event Manager",
                message=(
                    f"Hi {user.first_name},\n\n"
                    f"You've successfully RSVP'd to: {instance.name} on {instance.date} at {instance.time}.\n\n"
                    f"Location: {instance.location}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )
