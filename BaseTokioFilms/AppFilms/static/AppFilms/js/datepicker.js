const input = document.getElementById("datepicker");

input.addEventListener("input", (e) => {
  let value = e.target.value.replace(/\D/g, ""); // Elimina caracteres no numéricos
  const day = value.slice(0, 2); // Primeros 2 dígitos son el día
  const month = value.slice(2, 4); // Siguientes 2 dígitos son el mes
  const year = value.slice(4, 8); // Resto son el año

  // Construye el valor formateado
  let formattedValue = day;
  if (month) formattedValue += "/" + month;
  if (year) formattedValue += "/" + year;

  e.target.value = formattedValue; // Actualiza el valor del input
});

input.addEventListener("blur", () => {
  const value = input.value;
  const parts = value.split("/");
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10);
  const year = parseInt(parts[2], 10);

  // Validar día, mes y año
  if (
    parts.length === 3 &&
    day >= 1 &&
    day <= 31 &&
    month >= 1 &&
    month <= 12 &&
    year >= 1000 &&
    year <= 9999
  ) {
    input.setCustomValidity("");
  } else {
    input.setCustomValidity(
      "Por favor, ingresa una fecha válida en formato dd/mm/yyyy"
    );
  }
});
