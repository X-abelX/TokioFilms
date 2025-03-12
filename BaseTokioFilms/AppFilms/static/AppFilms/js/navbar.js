document.addEventListener("DOMContentLoaded", function () {
  const mobileMenuButton = document.querySelector(
    '[aria-controls="mobile-menu"]'
  );
  const mobileMenu = document.getElementById("mobile-menu");

  // Asegurarse de que el menú móvil está oculto al principio
  mobileMenu.classList.add("hidden");

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden"); // Alterna la visibilidad del menú
    });
  }

  const userMenuButton = document.getElementById("user-menu-button");
  const userMenu = document.getElementById("user-menu");

  if (userMenuButton && userMenu) {
    userMenuButton.addEventListener("click", function (event) {
      event.stopPropagation();
      userMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", function (event) {
      if (
        !userMenu.contains(event.target) &&
        !userMenuButton.contains(event.target)
      ) {
        userMenu.classList.add("hidden");
      }
    });
  }
});
