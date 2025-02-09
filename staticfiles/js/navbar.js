// Get the hamburger and nav-links elements
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

// Add a click event listener to the hamburger menu
hamburger.addEventListener('click', () => {
  // Toggle the 'active' class on both hamburger and nav-links
  hamburger.classList.toggle('active');
  navLinks.classList.toggle('active');
});




// Get the navbar element
const navbar = document.querySelector('.navbar');

// Function to change the navbar background on scroll
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) { // You can adjust this threshold value
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});