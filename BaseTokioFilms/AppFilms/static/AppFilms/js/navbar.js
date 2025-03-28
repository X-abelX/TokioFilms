document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu elements
  const mobileMenuButton = document.getElementById('mobileMenuButton');
  const closeMobileMenuButton = document.getElementById('closeMobileMenu');
  const mobileMenu = document.getElementById('mobileMenu');
  const overlay = document.getElementById('overlay');

  // User dropdown elements
  const userProfileButton = document.getElementById('userProfileButton');
  const userDropdown = document.getElementById('userDropdown');

  // Verify all elements exist
  if (!mobileMenuButton || !closeMobileMenuButton || !mobileMenu || !overlay || 
      !userProfileButton || !userDropdown) {
    console.error('Navbar Error: One or more required elements are missing');
    return;
  }

  // Mobile menu functionality
  mobileMenuButton?.addEventListener('click', () => {
    mobileMenu?.classList.add('mobile-menu-open');
    mobileMenu?.classList.remove('mobile-menu-closed');
    overlay?.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  });

  // Close mobile menu
  function closeMobileMenu() {
    mobileMenu.classList.remove('mobile-menu-open');
    mobileMenu.classList.add('mobile-menu-closed');
    overlay.classList.add('hidden');
    document.body.style.overflow = ''; // Restore scrolling
  }

  closeMobileMenuButton.addEventListener('click', closeMobileMenu);
  overlay.addEventListener('click', closeMobileMenu);

  // Toggle user dropdown
  userProfileButton.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent event from bubbling to document
    userDropdown.classList.toggle('hidden');
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!userProfileButton.contains(e.target) && !userDropdown.contains(e.target)) {
      userDropdown.classList.add('hidden');
    }
  });

  // Navbar background effect on scroll
  const navbar = document.querySelector('nav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('bg-netflix-black/90', 'backdrop-blur-md', 'shadow-md');
      navbar.classList.remove('bg-gradient-to-b', 'from-black/80', 'to-transparent');
    } else {
      navbar.classList.remove('bg-netflix-black/90', 'backdrop-blur-md', 'shadow-md');
      navbar.classList.add('bg-gradient-to-b', 'from-black/80', 'to-transparent');
    }
  });
});