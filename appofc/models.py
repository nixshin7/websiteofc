# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Photo Categories'


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to Category model
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Gallery Photos'
    

    
class VideoCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Video Categories'


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    video_category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)  # Make sure this is here
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Gallery Videos'



from django.db import models  # Import this line if you are using models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_pics/default.jpg')
    background_image = models.ImageField(upload_to='background_images/', default='background_pics/default_bg.jpg')
    bio = models.TextField(blank=True, null=True)  # Ensure this field is included

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Created Profiles'

    

from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default_image.jpg')  # Set a default value

    # or, if you want to make it non-nullable:
    image = models.ImageField(upload_to='profile_pics/', blank=False, null=True)  # Make sure you set an actual default for existing rows

    def __str__(self):
        return self.user.username
