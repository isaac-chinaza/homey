from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import MaintenanceRequest
from notifications.models import Notification

User = get_user_model()


def get_admin_users():
    return User.objects.filter(role="admin", is_active=True)


@receiver(pre_save, sender=MaintenanceRequest)
def track_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = MaintenanceRequest.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except MaintenanceRequest.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=MaintenanceRequest)
def notify_status_change(sender, instance, created, **kwargs):
    link = f"/maintenance/{instance.id}/"
    if created:
        recipients = {}

        if instance.property.owner:
            recipients[instance.property.owner.id] = (
                instance.property.owner,
                f"New maintenance request: {instance.title} at {instance.property.name}.",
            )

        if instance.property.manager:
            recipients[instance.property.manager.id] = (
                instance.property.manager,
                f"New maintenance request: {instance.title} at {instance.property.name}.",
            )

        if instance.tenant:
            recipients[instance.tenant.id] = (
                instance.tenant,
                f"We received your maintenance request: {instance.title}.",
            )

        for admin in get_admin_users():
            recipients[admin.id] = (
                admin,
                f"Maintenance request created: {instance.title} at {instance.property.name}.",
            )

        Notification.objects.bulk_create(
            [
                Notification(user=user, message=msg, link=link)
                for user, msg in recipients.values()
            ]
        )
    else:
        if hasattr(instance, "_old_status") and instance._old_status != instance.status:
            recipients = {}

            if instance.tenant:
                recipients[instance.tenant.id] = (
                    instance.tenant,
                    f"Your maintenance request '{instance.title}' is now {instance.get_status_display()}.",
                )

            if instance.property.owner:
                recipients[instance.property.owner.id] = (
                    instance.property.owner,
                    f"Request '{instance.title}' at {instance.property.name} is now {instance.get_status_display()}.",
                )

            if instance.property.manager:
                recipients[instance.property.manager.id] = (
                    instance.property.manager,
                    f"Request '{instance.title}' at {instance.property.name} is now {instance.get_status_display()}.",
                )

            for admin in get_admin_users():
                recipients.setdefault(
                    admin.id,
                    (
                        admin,
                        f"Maintenance request '{instance.title}' status changed to {instance.get_status_display()}.",
                    ),
                )

            Notification.objects.bulk_create(
                [
                    Notification(user=user, message=msg, link=link)
                    for user, msg in recipients.values()
                ]
            )
