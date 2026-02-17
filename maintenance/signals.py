from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import MaintenanceRequest
from notifications.models import Notification

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
    if created:
        recipient = instance.property.manager if instance.property.manager else instance.property.owner
        if recipient:
            Notification.objects.create(
                user=recipient,
                message=f"New maintenance request: {instance.title} for {instance.property.name}",
                link=f"/maintenance/{instance.id}/"
            )
    else:
        if hasattr(instance, '_old_status') and instance._old_status != instance.status:
            Notification.objects.create(
                user=instance.tenant,
                message=f"Maintenance request '{instance.title}' status updated to {instance.get_status_display()}",
                link=f"/maintenance/{instance.id}/"
            )
