from django.core.cache import cache
from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        cache_key = f"notifications:summary:{request.user.id}"
        data = cache.get(cache_key)
        if data is None:
            unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
            recent_notifications = list(
                Notification.objects.filter(user=request.user).order_by("-created_at")[:5]
            )
            data = {
                "unread_notifications_count": unread_count,
                "recent_notifications": recent_notifications,
            }
            cache.set(cache_key, data, 60)
        return {
            "unread_notifications_count": data["unread_notifications_count"],
            "recent_notifications": data["recent_notifications"],
        }
    return {}
