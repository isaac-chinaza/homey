from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Property
from notifications.models import Notification

User = get_user_model()


def get_admin_users():
    return User.objects.filter(role="admin", is_active=True)


@receiver(post_save, sender=Property)
def notify_property_created(sender, instance, created, **kwargs):
    if not created:
        return

    link = f"/properties/{instance.id}/"
    recipients = {}

    if instance.owner:
        recipients[instance.owner.id] = (
            instance.owner,
            f"Property '{instance.name}' was added to your portfolio.",
        )

    if instance.manager:
        recipients[instance.manager.id] = (
            instance.manager,
            f"You are assigned as manager for '{instance.name}'.",
        )

    for admin in get_admin_users():
        recipients[admin.id] = (
            admin,
            f"New property '{instance.name}' added to the system.",
        )

    Notification.objects.bulk_create(
        [
            Notification(user=user, message=msg, link=link)
            for user, msg in recipients.values()
        ]
    )

