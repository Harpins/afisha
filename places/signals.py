from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Image
from django.db.models import Max


@receiver(pre_save, sender=Image)
def set_auto_ordinal(sender, instance, **kwargs):
    if not instance.ordinal:
        max_ordinal = Image.objects.filter(location=instance.location).aggregate(
            Max("ordinal")
        )["ordinal__max"]
        instance.ordinal = (max_ordinal + 1) if max_ordinal else 1
