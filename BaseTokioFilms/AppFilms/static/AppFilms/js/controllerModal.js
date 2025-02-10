document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("default-modal");
  const openModalButton = document.getElementById("open-modal");
  const closeModalButtons = document.querySelectorAll(
    '[data-modal-hide="default-modal"]'
  );

  // Abre el modal cuando se hace clic en el botón
  openModalButton.addEventListener("click", () => {
    modal.classList.remove("hidden"); // Elimina la clase hidden para mostrar el modal
    modal.removeAttribute("inert"); // Elimina el atributo inert
  });

  // Cierra el modal cuando se hace clic en el botón de cerrar
  closeModalButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modal.classList.add("hidden"); // Vuelve a agregar la clase hidden para ocultar el modal
      modal.setAttribute("inert", ""); // Agrega el atributo inert
    });
  });
});
