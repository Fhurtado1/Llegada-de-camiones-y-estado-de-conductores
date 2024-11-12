async function obtenerConductores() {
    try {
        const response = await fetch('http://127.0.0.1:5000/conductores');
        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }
        const conductores = await response.json();

        const tabla = document.getElementById('tabla-conductores');
        tabla.innerHTML = ''; // Limpiar la tabla antes de agregar filas

        conductores.forEach(conductor => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${conductor.nombre}</td>
                <td>${conductor.dni}</td>
                <td>${conductor.placa}</td>
                <td>${conductor.ubicacion}</td>
                <td>${conductor.hora_entrada}</td>
                <td>
                    <button onclick="registrarSalida(${conductor.id})">Registrar Salida</button>
                </td>
            `;
            tabla.appendChild(fila);
        });
    } catch (error) {
        console.error("Error al obtener conductores:", error);
        alert("Hubo un problema al cargar los datos de conductores.");
    }
}

async function registrarSalida(id) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/conductores/${id}/salida`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }
        alert("Salida registrada correctamente.");
        obtenerConductores(); // Refresca la lista de conductores
    } catch (error) {
        console.error("Error al registrar salida:", error);
        alert("Hubo un problema al registrar la salida.");
    }
}

// Llama a la función para cargar los conductores cuando la página se cargue
window.onload = obtenerConductores;
