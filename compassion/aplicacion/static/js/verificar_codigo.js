function checkCodigoAvailability(input) {
  var codigoInput = input;
  var codigoAvailability = document.getElementById("codigo-availability");

  fetch(`/verificar_codigo/?codigo=${codigoInput.value}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.exists) {
        codigoAvailability.textContent = "El código ya existe";
        codigoInput.setCustomValidity("El código ya existe");
      } else {
        codigoAvailability.textContent = ""; // Limpiar el mensaje
        codigoInput.setCustomValidity(""); // Limpiar el mensaje de validación
      }
    })
    .catch((error) => {
      console.error("Error al verificar el código:", error);
    });
}
