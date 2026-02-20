from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


def invalidate_user_cache(user_id):
    cache_key = f"notifications:summary:{user_id}"
    cache.delete(cache_key)


def broadcast_notification(user_id, message, link):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    unread = Notification.objects.filter(user_id=user_id, is_read=False).count()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "notification.message",
            "message": message,
            "link": link,
            "unread": unread,
        },
    )


@receiver(post_save, sender=Notification)
def notification_saved(sender, instance, created, **kwargs):
    if instance.user_id:
        invalidate_user_cache(instance.user_id)
        broadcast_notification(instance.user_id, instance.message, instance.link or "#")


@receiver(post_delete, sender=Notification)
def notification_deleted(sender, instance, **kwargs):
    if instance.user_id:
        invalidate_user_cache(instance.user_id)
        # Broadcast count change
        broadcast_notification(instance.user_id, "Notification updated.", "#")
