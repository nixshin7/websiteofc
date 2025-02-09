from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from appofc.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the profile already exists
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



# Delete category in Django administration if they are 0
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Photo, Category

@receiver(post_delete, sender=Photo)
def delete_empty_categories(sender, instance, **kwargs):
    # Ensure that the instance has a valid category and the category still exists
    if instance.category:
        try:
            # Try to fetch the category from the database (to handle deleted categories)
            category = Category.objects.get(id=instance.category.id)
            
            # Check if there are any other photos in the same category
            if not Photo.objects.filter(category=category).exists():
                # If no photos are left, delete the category
                category.delete()
        except Category.DoesNotExist:
            # If the category was deleted already, simply pass (nothing to do)
            pass



