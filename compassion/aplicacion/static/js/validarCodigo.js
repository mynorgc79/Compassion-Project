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
