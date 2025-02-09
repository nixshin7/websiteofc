from django.contrib import admin
from .models import Photo, Profile, Category, Video, VideoCategory, Member

# Register your models here.

# Customizing the Photo model in the admin interface
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')  # Customize fields to display
    search_fields = ('title',)  # Add search functionality

    def delete_queryset(self, request, queryset):
        # Deletes without confirmation
        queryset.delete()



admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(VideoCategory)
admin.site.register(Member)