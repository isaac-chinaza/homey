from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Tenant
from notifications.models import Notification

User = get_user_model()


def get_admin_users():
    return User.objects.filter(role="admin", is_active=True)


@receiver(post_save, sender=Tenant)
def notify_tenant_events(sender, instance, created, **kwargs):
    link = "/dashboard/"
    recipients = {}

    if created:
        if instance.user:
            recipients[instance.user.id] = (
                instance.user,
                "Your tenancy is now active.",
            )

        if instance.property and instance.property.owner:
            recipients[instance.property.owner.id] = (
                instance.property.owner,
                f"New tenant added to {instance.property.name}.",
            )

        if instance.property and instance.property.manager:
            recipients[instance.property.manager.id] = (
                instance.property.manager,
                f"New tenant added to {instance.property.name}.",
            )

        for admin in get_admin_users():
            recipients[admin.id] = (
                admin,
                f"Tenant added for {instance.property.name if instance.property else 'a property'}.",
            )

        Notification.objects.bulk_create(
            [
                Notification(user=user, message=msg, link=link)
                for user, msg in recipients.values()
            ]
        )

