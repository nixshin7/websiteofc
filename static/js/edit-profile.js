document.addEventListener("DOMContentLoaded", function() {
    // Get the elements for profile and background buttons
    const profileButton = document.getElementById("change-profile-btn");
    const backgroundButton = document.getElementById("change-background-btn");

    const profileInput = document.getElementById("profile_image");
    const backgroundInput = document.getElementById("background_image");

    // When the profile button is clicked, trigger the file input
    profileButton.addEventListener("click", function() {
        profileInput.click();
    });

    // When the background button is clicked, trigger the file input
    backgroundButton.addEventListener("click", function() {
        backgroundInput.click();
    });
});


// Function to preview the profile image
function previewProfileImage() {
    const file = document.getElementById('profile_image').files[0];
    const preview = document.getElementById('profile-image-preview');

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            preview.style.backgroundImage = 'url(' + e.target.result + ')';
        }

        reader.readAsDataURL(file);
    }
}

// Function to preview the background image
function previewBackgroundImage() {
    const file = document.getElementById('background_image').files[0];
    const preview = document.getElementById('background-image-preview');

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            preview.style.backgroundImage = 'url(' + e.target.result + ')';
        }

        reader.readAsDataURL(file);
    }
}

