from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def invalidate_user_menu(sender, instance, **kwargs):
    cache.delete(f"menu:{instance.id}")
