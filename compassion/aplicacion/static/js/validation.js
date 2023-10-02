//validar longitud de numero telefonico.
export function validarLongitud(input, maxLength, errorId) {
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

export function validateLetters(input, errorId) {
  var lettersRegex = /^[a-zA-Z\s]*$/; // Expresión regular para letras y espacios
  var errorMessageElement = document.getElementById(errorId);

  if (!input.value.match(lettersRegex)) {
    errorMessageElement.innerHTML =
      "Solo se permiten letras y espacios en blanco.";
    input.setCustomValidity("Solo se permiten letras y espacios en blanco.");
  } else {
    errorMessageElement.innerHTML = "";
    input.setCustomValidity("");
  }
}

// Función para validar que el valor solo contenga números
// Validación para el campo "codigo" (aceptar solo números)

const codigoInput = document.getElementById("codigo");
const codigoError = document.getElementById("codigo-error");

codigoInput.addEventListener("input", function (e) {
  const codigoValue = e.target.value;
  if (!/^\d+$/.test(codigoValue)) {
    codigoError.textContent = "Solo se permiten números.";
    codigoInput.setCustomValidity("Solo se permiten números.");
  } else {
    codigoError.textContent = "";
    codigoInput.setCustomValidity("");
  }
});

function validateNumbers(input, errorId) {
  var numbersRegex = /^[0-9]*$/; // Expresión regular para números
  var errorMessageElement = document.getElementById(errorId);

  if (!input.value.match(numbersRegex)) {
    errorMessageElement.innerHTML = "Solo se permiten números.";
    input.setCustomValidity("Solo se permiten números.");
  } else {
    errorMessageElement.innerHTML = "";
    input.setCustomValidity("");
  }
}
