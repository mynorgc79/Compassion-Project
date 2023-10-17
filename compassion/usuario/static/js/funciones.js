<script>
$(document).ready(function() {
    // Agrega un controlador de eventos de cambio a los checkboxes
    $('.custom-switch-input').on('change', function() {
        var checkbox = $(this);
        var usuarioId = checkbox.attr('id').replace('estado', '');
        var estado = checkbox.prop('checked');

        // Realiza una solicitud AJAX para actualizar el estado en el servidor
        $.ajax({
            type: 'POST',
            url: '/actualizar_estado_usuario/',  // Reemplaza con la URL correcta de tu vista de Django
            data: {
                usuario_id: usuarioId,
                estado: estado ? 'activo' : 'inactivo',
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                if (data.success) {
                    // El estado se ha actualizado con éxito, muestra un mensaje o realiza otras acciones
                } else {
                    // Ha ocurrido un error al actualizar el estado, muestra un mensaje de error o realiza otras acciones
                }
            },
            error: function() {
                // Ha ocurrido un error al realizar la solicitud AJAX, muestra un mensaje de error o realiza otras acciones
            }
        });
    })};
);
</script>