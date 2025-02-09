from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Photo, Profile, Category, Member  # Make sure Profile is defined if used


# Photo Upload Form
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'photo', 'category']  # Include category

    # You can specify a queryset here to show categories dynamically
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-control'}))



from .models import Video, VideoCategory

class VideoUploadForm(forms.ModelForm):
    custom_category = forms.CharField(max_length=50, required=False)  # Optional custom category field
    description = forms.CharField(widget=forms.Textarea, required=False)  # Add description field

    class Meta:
        model = Video
        fields = ['title', 'video', 'video_category', 'description']

    def clean_video_category(self):
        category = self.cleaned_data.get('video_category')
        custom_category = self.cleaned_data.get('custom_category')

        # If 'Other' is selected and no custom category is provided, raise an error
        if category == 'Other' and not custom_category:
            raise forms.ValidationError('Please provide a custom category name.')

        if category == 'Other' and custom_category:
            # If 'Other' is selected and the user provided a custom category
            # Create the custom category if it doesn't exist
            video_category, created = VideoCategory.objects.get_or_create(name=custom_category)
            return video_category  # Return the newly created category or existing one

        return category  # Otherwise, return the selected category


from django import forms
from .models import Profile, Member

# Profile Update Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'background_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write about yourself...'}),  # Custom placeholder
        }

    def save(self, commit=True):
        profile = super().save(commit=False)  # Save the profile but don't commit yet
        if commit:
            profile.save()  # Save the profile object to the database

            # Update the corresponding Member record when the profile image is updated
            try:
                # Get the Member associated with the user
                member = Member.objects.get(user=profile.user)
                # Update the Member's image field with the Profile's profile_image
                member.image = profile.profile_image
                member.save()
            except Member.DoesNotExist:
                # If the Member does not exist, you can create a new one or handle this case as needed
                pass

        return profile




from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    username = forms.CharField(
        max_length=150,
        label="Username",
        help_text="Username can contain letters, numbers, spaces, and @/./+/-/_ characters.",
    )

    class Meta:
        model = get_user_model()  # Use the custom user model here
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        
        # Check if the username is valid: letters, numbers, spaces, and allowed special characters, 
        # but no leading or trailing spaces
        if not re.match(r'^[a-zA-Z0-9\-_ ]+$', username) or username != username.strip():
            raise ValidationError("Username can only contain letters, numbers, spaces, and -/_ characters, and cannot start or end with a space.")
            
        # Check for unique username (case insensitive)
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise ValidationError('Username already exists.')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
    
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError('This email already taken.')

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError("Passwords do not match.")
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()

            # Check if Profile already exists and create it if not
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

            # Create Member only if it doesn't exist
            if not hasattr(user, 'member'):
                Member.objects.create(user=user, role='New Member', image=user.profile.profile_image)

        return user




from django import forms
from .models import Member

class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['role', 'image']  # Add the 'user', 'role', and 'image' fields















