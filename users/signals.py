from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, PassengerProfile, RailwayStaffProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "passenger":
            PassengerProfile.objects.create(user=instance)
        elif instance.user_type == "railway_staff":
            RailwayStaffProfile.objects.create(user=instance)
