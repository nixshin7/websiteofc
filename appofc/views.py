from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegistrationForm, ProfileForm, MemberForm

from appofc.models import Profile, Photo, Category
from django.contrib.auth.models import User
from .forms import VideoUploadForm
from .models import VideoCategory, Video

# Create your views here.

# Home View
def home(request):
    return render(request, 'content/home.html')



from django.shortcuts import render
from .models import Member

def members(request):
    members = Member.objects.all()  # This fetches all member objects
    # Log the number of members to confirm if new members are being fetched
    print(f"Total members: {members.count()}")
    return render(request, 'content/members.html', {'members': members})





# Gallery View
def gallery(request):
    users = User.objects.all()
    photos = Photo.objects.all()

    # Fetch categories by accessing the name of the Category model
    categories = Category.objects.filter(photo__isnull=False).distinct()

    user_id = request.GET.get('user')
    if user_id:
        photos = photos.filter(user_id=user_id)

    selected_category = request.GET.get('category')
    if selected_category:
        photos = photos.filter(category__id=selected_category)  # Filter photos by category ID

    date = request.GET.get('date')
    if date:
        photos = photos.filter(uploaded_at__date=date)

    context = {
        'photos': photos,
        'users': users,
        'categories': categories,  # Now passing Category objects
        'date': date,
    }

    return render(request, 'content/gallery.html', context)



def video_gallery(request):
    # Get all videos to display
    videos = Video.objects.all()

    return render(request, "content/video-gallery.html", {"videos": videos})






# Contact View
def contact(request):
    return render(request, "content/contact.html")


def upload_photo(request):
    # Get categories that have at least one photo
    categories = Category.objects.filter(photo__isnull=False).distinct()  # Ensure no duplicates

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')  # Selected category
        custom_category = request.POST.get('custom_category')  # Custom category if "Other" is selected
        photo = request.FILES.get('photo')

        # If "Other" is selected and a custom category is provided
        if category_id == 'Other' and custom_category:
            # Check if a category with the custom name already exists
            existing_category = Category.objects.filter(name=custom_category).first()
            if existing_category:
                # If the category exists, use it
                category = existing_category
            else:
                # If the category doesn't exist, create a new one
                category = Category(name=custom_category)
                category.save()
        elif category_id != 'Other':  # If a predefined category is selected
            # Check if the category exists in the database before using it
            category = Category.objects.get(id=category_id)

        # Save the photo with the selected category
        photo_instance = Photo.objects.create(
            user=request.user,
            title=title,
            photo=photo,
            category=category
        )

        photo_instance.save()

        messages.success(request, 'Your photo has been uploaded successfully!')
        return redirect('gallery')  # Redirect to the gallery to show the new photo

    return render(request, 'upload-content/upload-photo.html', {'categories': categories})










def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_category_id = request.POST.get('video_category')
        custom_category = request.POST.get('custom_category', None)  # If there's a custom category
        video = request.FILES.get('video')
        description = request.POST.get('description')  # Get description from the form

        # If custom category is chosen, use it; otherwise, use selected category
        if video_category_id == 'Other' and custom_category:
            video_category = VideoCategory.objects.create(name=custom_category)
        else:
            video_category = VideoCategory.objects.get(id=video_category_id)

        # Create the Video object and save it
        new_video = Video.objects.create(
            user=request.user,
            title=title,
            video=video,
            video_category=video_category,
            description=description  # Save the description here
        )

        return redirect('video_gallery')  # Redirect to the video gallery after upload

    # If it's a GET request, pass categories to the template
    video_categories = VideoCategory.objects.all()
    return render(request, 'upload-content/upload-video.html', {'video_categories': video_categories})




# Registration View
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        if username and password:
            try:
                user = User.objects.get(username__iexact=username)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'The password is incorrect.')
            except User.DoesNotExist:
                messages.error(request, 'The username does not exist.')
        else:
            messages.error(request, 'Both username and password are required.')

    return render(request, 'auth/login.html', {'form': AuthenticationForm()})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')


# Profile View (Requires Login)
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'auth/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    try:
        # Fetch the Profile associated with the logged-in user
        profile = request.user.profile
    except Profile.DoesNotExist:
        # If no Profile exists for the user, handle this case as needed
        return redirect('create-profile')  # Redirect to a profile creation page if necessary
    
    if request.method == 'POST':
        # If it's a POST request, bind the form to the profile instance
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the form data to the Profile model
            return redirect('profile')  # Redirect to the user's profile page after update
    else:
        # If it's a GET request, pre-populate the form with the current profile data
        form = ProfileForm(instance=profile)

    # Render the 'edit-profile.html' template and pass the form to the context
    return render(request, 'auth/edit-profile.html', {'form': form})



@login_required
def update_member(request):
    user = request.user

    # Check if more than one Member exists for this user (even though it shouldn't happen)
    members = Member.objects.filter(user=user)
    if members.count() > 1:
        members.exclude(id=members.first().id).delete()  # Delete all duplicates, keeping the first one
    
    # Get or create a single member
    member = members.first()

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()  # Save the updated member data (including profile image and role)
            return redirect('members')  # Redirect back to the members page
    else:
        form = MemberForm(instance=member)  # Pre-fill the form with the current member data

    return render(request, 'content/update_member.html', {'form': form})