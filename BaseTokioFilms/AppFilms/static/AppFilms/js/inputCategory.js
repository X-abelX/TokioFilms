document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-film-form");
  const categorySelect = document.getElementById("category");

  form.addEventListener("submit", (event) => {
    if (categorySelect.value === "null") {
      event.preventDefault();
      alert(
        "No hay categorías disponibles. Por favor, añade una categoría primero."
      );
    }
  });
});
