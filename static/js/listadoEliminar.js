
        const URL = "http://127.0.0.1:5000/"

        //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        //const URL = "https://andreag.pythonanywhere.com/"
        
        // Obtiene el contenido del inventario
        function obtenerMenu() {
            fetch(URL + 'menu') // Realiza una solicitud GET al servidor y obtener la lista de menues.
                .then(response => {
                    // Si es exitosa (response.ok), convierte los datos de la respuesta de formato JSON a un objeto JavaScript.
                    if (response.ok) { return response.json(); }
                })
                // Asigna los datos de los menues obtenidos a la propiedad menues del estado.
                .then(data => {
                    const menuTable = document.getElementById('menu-table').getElementsByTagName('tbody')[0];
                    menuTable.innerHTML = ''; // Limpia la tabla antes de insertar nuevos datos
                    data.forEach(menu => {
                        const row = menuTable.insertRow();
                        row.innerHTML = `
                            <td>${menu.codigo}</td>
                            <td>${menu.descripcion}</td>
                            <td align="right">${menu.precio}</td>
                            <td><button onclick="eliminarMenu('${menu.codigo}')">Eliminar</button></td>
                        `;
                    });
                })
                // Captura y maneja errores, mostrando una alerta en caso de error al obtener los menues.
                .catch(error => {
                    console.log('Error:', error);
                    alert('Error al obtener los menues.');
                });
        }

        // Se utiliza para eliminar un menu.
        function eliminarMenu(codigo) {
            // Se muestra un diálogo de confirmación. Si el usuario confirma, se realiza una solicitud DELETE al servidor a través de fetch(URL + 'menu/${codigo}', {method: 'DELETE' }).
            if (confirm('¿Estás seguro de que quieres eliminar este Menu?')) {
                fetch(URL + `menu/${codigo}`, { method: 'DELETE' })
                    .then(response => {
                        if (response.ok) {
                            // Si es exitosa (response.ok), elimina el menu y da mensaje de ok.
                            obtenerMenu(); // Vuelve a obtener la lista de menu para actualizar la tabla.
                            alert('Menu eliminado correctamente.');
                        }
                    })
                    // En caso de error, mostramos una alerta con un mensaje de error.
                    .catch(error => {
                        alert(error.message);
                    });
            }
        }

        // Cuando la página se carga, llama a obtenerMenu para cargar la lista de menues.
        document.addEventListener('DOMContentLoaded', obtenerMenu);
    