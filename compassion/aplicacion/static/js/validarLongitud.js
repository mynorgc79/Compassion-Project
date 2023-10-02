//validar longitud de numero telefonico.
function validarLongitud(input, maxLength, errorId) {
  const valor = input.value.trim();
  const errorElement = document.getElementById(errorId);

  if (valor.length > maxLength) {
    errorElement.textContent = "Solo se permiten 8 dígitos.";
    input.setCustomValidity("Solo se permiten 8 dígitos.");
    input.value = valor.substring(0, maxLength); // Recortar a 8 dígitos
  } else {
    errorElement.textContent = "";
    input.setCustomValidity("");
  }
}
