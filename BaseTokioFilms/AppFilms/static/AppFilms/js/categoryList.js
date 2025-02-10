document.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("list");
    let draggedItem = null;
    let editedCategories = {};
    let categoryIdToDelete = null;
  
    // Funciones de manejo de arrastre
    function handleDragStart(e) {
      if (this.querySelector(".edit-mode").classList.contains("hidden")) {
        draggedItem = this;
        this.classList.add("opacity-50");
        e.dataTransfer.effectAllowed = "move";
      }
    }
  
    function handleDragOver(e) {
      e.preventDefault();
      const bounding = this.getBoundingClientRect();
      const offset = e.clientY - bounding.top;
      try {
        if (this !== draggedItem) {
          if (offset > bounding.height / 2) {
            this.parentNode.insertBefore(draggedItem, this.nextSibling);
          } else {
            this.parentNode.insertBefore(draggedItem, this);
          }
        }
      } catch (error) {
        // Manejar el error sin mostrarlo en la consola
      }
    }
  
    function handleDrop(e) {
      e.preventDefault();
      if (draggedItem) {
        draggedItem.classList.remove("opacity-50");
        updateOrder(); // Llamada a la función que actualiza el orden
      }
    }
  
    function handleDragEnd() {
      this.classList.remove("opacity-50");
    }
  
    // Función para adjuntar los eventos de arrastre
    function attachDragEvents(item) {
      item.addEventListener("dragstart", handleDragStart);
      item.addEventListener("dragover", handleDragOver);
      item.addEventListener("drop", handleDrop);
      item.addEventListener("dragend", handleDragEnd);
    }
  
    // Modo edición: mostrar/ocultar el input y desactivar el arrastre mientras se edita
    function startEdit(div) {
      const parent = div.closest("[data-id]");
      const editMode = parent.querySelector(".edit-mode");
      const span = parent.querySelector("span");
      const input = editMode.querySelector("input");
      editMode.classList.remove("hidden");
      span.classList.add("hidden");
      input.value = span.textContent;
      input.focus();
      parent.draggable = false; // Desactivamos arrastre mientras editamos
    }
  
    function saveEdit(parent, input, span, editMode) {
      // Ocultar el input y mostrar el span con el nuevo valor
      editMode.classList.add("hidden");
      span.classList.remove("hidden");
      span.textContent = input.value;
  
      // Guardar el cambio en el servidor
      const categoryId = parent.dataset.id;
      const newName = input.value;
  
      fetch(`${urls.updateCategoryName}${categoryId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({ name: newName }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            console.log("Nombre actualizado correctamente");
          } else {
            alert("Error al actualizar el nombre");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Error al actualizar el nombre");
        });
  
      // Restauramos la capacidad de arrastrar
      parent.draggable = true;
      attachDragEvents(parent);
    }
  
    // Manejo del clic en el botón check (guardar)
    document.querySelectorAll(".edit-mode button").forEach((button) => {
      button.addEventListener("click", function (event) {
        event.stopPropagation(); // Evitamos que se propague y dispare otros eventos
        const parent = this.closest("[data-id]");
        const editMode = parent.querySelector(".edit-mode");
        const span = parent.querySelector("span");
        const input = editMode.querySelector("input");
        saveEdit(parent, input, span, editMode);
      });
    });
  
    // Si se hace clic fuera de un elemento en edición, se guarda la edición
    document.addEventListener("click", (event) => {
      if (!event.target.closest("[data-id]")) {
        document.querySelectorAll(".edit-mode").forEach((editMode) => {
          if (!editMode.classList.contains("hidden")) {
            const parent = editMode.closest("[data-id]");
            const input = editMode.querySelector("input");
            const span = parent.querySelector("span");
            saveEdit(parent, input, span, editMode);
          }
        });
      }
    });
  
    // Al cargar la página, adjuntamos los eventos de arrastre a todos los elementos
    document.querySelectorAll("[data-id]").forEach((item) => {
      item.draggable = true;
      attachDragEvents(item); // Aseguramos de que los elementos tengan los eventos de arrastre
    });
  
    // Permitir iniciar la edición al hacer clic en el span
    document.querySelectorAll("[data-id] span").forEach((span) => {
      span.addEventListener("click", () => startEdit(span)); // Se invoca startEdit correctamente
    });
  
    // Definir funciones auxiliares que faltaban
    function updateOrder() {
      const items = document.querySelectorAll("[data-id]");
      const order = Array.from(items).map((item, index) => ({
        id: item.dataset.id,
        position: index + 1,
      }));
  
      fetch(urls.updateOrder, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({ order }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            console.log("Orden actualizado correctamente");
          } else {
            alert("Error al actualizar el orden");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Error al actualizar el orden");
        });
    }
  
    // Abrir modal de eliminación
    document.querySelectorAll(".open-delete-modal").forEach((button) => {
      button.addEventListener("click", function () {
        categoryIdToDelete = this.dataset.id;
        document.querySelector("#modal2 input").value = ""; // Limpiar el input al abrir el modal
        modal2.classList.remove("hidden");
      });
    });
  
    // Cerrar modal de eliminación
    document.getElementById("closeModal2").addEventListener("click", () => {
      document.querySelector("#modal2 input").value = ""; // Limpiar el input al cerrar el modal
      modal2.classList.add("hidden");
    });
  
    document.getElementById("cancelModal2").addEventListener("click", () => {
      document.querySelector("#modal2 input").value = ""; // Limpiar el input al cerrar el modal
      modal2.classList.add("hidden");
    });
  
    // Confirmar eliminación
    document.querySelector(".confirm-delete").addEventListener("click", () => {
      const confirmationInput = document.querySelector("#modal2 input").value.trim();
      if (confirmationInput === "ELIMINAR" && categoryIdToDelete) {
        fetch(`${urls.deleteCategory}${categoryIdToDelete}/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              document.querySelector(`[data-id="${categoryIdToDelete}"]`).remove();
              document.querySelector("#modal2 input").value = ""; // Limpiar el input al cerrar el modal
              modal2.classList.add("hidden");
            } else {
              alert("Error al eliminar la categoría");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Error al eliminar la categoría");
          });
      } else {
        alert('Por favor, escriba "ELIMINAR" para confirmar.');
      }
    });
  
    // Añadir nueva categoría
    const addCategoryButton = document.getElementById("add-category-button");
    const newCategoryNameInput = document.getElementById("new-category-name");
  
    addCategoryButton.addEventListener("click", () => {
      const categoryName = newCategoryNameInput.value.trim();
      if (categoryName) {
        fetch(urls.addCategory, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
          body: JSON.stringify({ name: categoryName }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              const newCategory = document.createElement("div");
              newCategory.className = "bg-[#141414] rounded shadow-sm";
              newCategory.draggable = true;
              newCategory.dataset.id = data.id;
              newCategory.innerHTML = `
                <div class="flex items-center p-3 gap-2">
                  <button onclick="toggleEdit(this)" class="text-white hover:text-gray-300">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                  <div class="flex-1" data-id="${data.id}">
                    <span class="block text-white">${data.name}</span>
                    <div class="hidden edit-mode flex">
                      <input type="text" value="${data.name}" class="w-full bg-black text-white px-3 py-1 mr-2 rounded" data-id="${data.id}">
                      <button class="bg-green-500 text-white p-2 rounded-md hover:bg-green-600">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
                  <button class="p-2 bg-red-500 hover:bg-red-600 rounded-lg open-delete-modal" data-id="${data.id}">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="white" class="w-6 h-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 6h18M8 6v12m8-12v12M5 6l1 14a2 2 0 002 2h8a2 2 0 002-2l1-14M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2" />
                    </svg>
                  </button>
                </div>
              `;
              list.appendChild(newCategory);
              newCategoryNameInput.value = "";
  
              // Adjuntar eventos a la nueva categoría
              attachDragEvents(newCategory);
              newCategory.querySelector("span").addEventListener("click", () => startEdit(newCategory.querySelector("span")));
              newCategory.querySelector(".edit-mode button").addEventListener("click", function (event) {
                event.stopPropagation();
                const parent = this.closest("[data-id]");
                const editMode = parent.querySelector(".edit-mode");
                const span = parent.querySelector("span");
                const input = editMode.querySelector("input");
                saveEdit(parent, input, span, editMode);
              });
              newCategory.querySelector(".open-delete-modal").addEventListener("click", function () {
                categoryIdToDelete = this.dataset.id;
                document.querySelector("#modal2 input").value = "";
                modal2.classList.remove("hidden");
              });
            } else {
              alert("Error al añadir la categoría");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Error al añadir la categoría");
          });
      }
    });
  });