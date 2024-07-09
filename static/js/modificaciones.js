
        // const URL = "http://127.0.0.1:5000/"
        
        // Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        const URL = "https://andreag.pythonanywhere.com/"

        // Variables de estado para controlar la visibilidad y los datos del formulario
        let codigo = '';
        let descripcion = '';
        let precio = '';
        let mostrarDatosMenu = false;

        document.getElementById('form-obtener-menu').addEventListener('submit', obtenerMenu);
        document.getElementById('form-guardar-cambios').addEventListener('submit', guardarCambios);

        // Se ejecuta cuando se envía el formulario de consulta. Realiza una solicitud GET a la API y obtiene los datos del menu correspondiente al código ingresado.
        function obtenerMenu(event) {
            event.preventDefault();
            codigo = document.getElementById('codigo').value;
           
            fetch(URL + 'menu/' + codigo)
               
                .then(response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        throw new Error('Error al obtener los datos del menu.')
                    }
                })
                .then(data => {
                    descripcion = data.descripcion;
             
                    precio = data.precio;
                 
                    mostrarDatosMenu = true; //Activa la vista del segundo formulario
                    mostrarFormulario();
                })
                .catch(error => {
                    alert('Código no encontrado.');
                });
        }

        // Muestra el formulario con los datos del Menu
        function mostrarFormulario() {
            if (mostrarDatosMenu) {
                document.getElementById('descripcionModificar').value = descripcion;
                document.getElementById('precioModificar').value = precio;


                document.getElementById('datos-menu').style.display = 'block';
            } else {
                document.getElementById('datos-menu').style.display = 'none';
            }
        }

        

        // Se usa para enviar los datos modificados del Menu al servidor.
        function guardarCambios(event) {
            event.preventDefault();

            const formData = new FormData();
            formData.append('codigo', codigo);
            formData.append('descripcion', document.getElementById('descripcionModificar').value);
            formData.append('precio', document.getElementById('precioModificar').value);

            

            fetch(URL + 'menu/' + codigo, {
                method: 'PUT',
                body: formData,
            })
                .then(response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        throw new Error('Error al guardar los cambios del Menú.')
                    }
                })
                .then(data => {
                    alert('Menú actualizado correctamente.');
                    limpiarFormulario();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar el Menú.');
                });
        }

        // Restablece todas las variables relacionadas con el formulario a sus valores iniciales, lo que efectivamente "limpia" el formulario.
        function limpiarFormulario() {
            document.getElementById('codigo').value = '';
            document.getElementById('descripcionModificar').value = '';
            document.getElementById('precioModificar').value = '';



            codigo = '';
            descripcion = '';
            precio = '';
            mostrarDatosMenu = false;

            document.getElementById('datos-menu').style.display = 'none';
        }
    