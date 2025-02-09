"""
URL configuration for websiteofc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appofc import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),                                #Home URL
    path('members/', views.members, name='members'),                  #About URL
    path('update_member/', views.update_member, name='update_member'),# Update Member
    path('gallery/', views.gallery, name='gallery'),                  #Gallery URL
    path('contact/', views.contact, name='contact'),                  #Contact URL
    path('upload-photo/', views.upload_photo, name='upload_photo'),   #Contact URL
    path('upload-video/', views.upload_video, name='upload-video'),   #Upload Video URL
    path('video-gallery/', views.video_gallery, name='video_gallery'),#Video Gallery URL
    path('register/', views.register_view, name='register'),          #Register URL
    path('login/', views.login_view, name='login'),                   #Login URL
    path('logout/', views.logout_view, name='logout'),                #Logout URL
    path('profile/', views.profile, name='profile'),                  #Profile URL
    path('edit-profile/', views.edit_profile, name='edit_profile'),   #Edit-Profile-User URL
#   path('edit-profile/', views.edit_profile, name='edit_profile'),   #Edit-Profile URL

]


# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)