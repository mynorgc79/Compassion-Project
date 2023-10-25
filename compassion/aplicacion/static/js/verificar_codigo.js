   
function verificarCodigoExistente(input) {
  const codigoValue = input.value;

  if (codigoValue === '') {
    document.getElementById("codigo-availability").textContent = "El código no puede estar vacío.";
    return;
  }



  // Realiza la solicitud AJAX solo si el código es válido
  fetch(verificarCodigoUrl,  {
    method: "POST",
    body: new URLSearchParams({ 'codigo': codigoValue }),
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.existe) {
      document.getElementById("codigo-availability").textContent = "Este código ya existe.";
    } else {
      document.getElementById("codigo-availability").textContent = "";
    }
  });
}