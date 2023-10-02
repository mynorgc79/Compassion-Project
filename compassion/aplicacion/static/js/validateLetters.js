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
