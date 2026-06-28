// Aqui haremos la logica del buscador y de las evaluaciones.
// La idea es usar JavaScript para pedir datos a Spring Boot sin recargar la pagina.

// Primero sacamos el usuarioId de la URL.
// Esto viene desde Flask, por ejemplo: /buscar?usuarioId=1
const parametrosUrl = new URLSearchParams(window.location.search);
const usuarioId = parametrosUrl.get("usuarioId");

// Tomamos los elementos del HTML que vamos a ir cambiando.
// Esto es parecido a lo que ya habiamos hecho con los graficos,
// donde buscabamos un div o canvas por su id para despues modificarlo.
const input = document.getElementById("busqueda");
const mensaje = document.getElementById("mensaje");
const resultados = document.getElementById("resultados");
const imagenActividad = document.getElementById("imagen-actividad");

// Aqui guardamos las actividades que vienen desde Spring.
// Sirve para no tener que pedirlas de nuevo cada vez que se entra al detalle.
let actividadesActuales = [];

// Esta funcion limpia texto antes de meterlo como HTML.
// Es para evitar que algo escrito por un usuario se interprete como etiqueta HTML.
function escaparHTML(texto) {
    if (texto === null || texto === undefined) {return "";}
    return String(texto)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

// Siguiendo la misma logica que usamos en Flask,
// protegemos cosas raras con esta funcion.
// Si el texto trae signos como <, >, {{ }} o {% %}, no lo procesamos.
function tieneCodigoRaro(texto) {
    if (texto === null || texto === undefined) {return true;}

    if (texto.includes("<") || texto.includes(">")) {return true;}
    if (texto.includes("{{") || texto.includes("}}")) {return true;}
    if (texto.includes("{%") || texto.includes("%}")) {return true;}

    return false;
}

// Esta funcion marca en negrita la parte del texto que coincide con la busqueda.
// Por ejemplo, si busco "san", en "Santiago" marca esa parte.
function destacar(texto, busqueda) {
    const textoSeguro = escaparHTML(texto);
    if (busqueda.length < 3) {return textoSeguro;}

    // Esta parte evita problemas si la busqueda tiene simbolos raros.
    const busquedaEscapada = busqueda.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const expresion = new RegExp("(" + busquedaEscapada + ")", "gi");

    return textoSeguro.replace(expresion, "<strong>$1</strong>");
}

// Aqui armamos el historial de notas de una actividad.
// La informacion ya viene desde Spring como una lista con iniciales y nota.
function armarHistorial(historial) {
    if (!historial || historial.length === 0) {
        return `<p class="historial-vacio">Todavía no hay evaluaciones registradas.</p>`;
    }

    let html = `<div class="historial-notas">`;

    for (let i = 0; i < historial.length; i++) {
        html += `
            <span class="item-nota">
                ${escaparHTML(historial[i].iniciales)}: ${escaparHTML(historial[i].nota)}
            </span>
        `;
    }

    html += `</div>`;
    return html;
}

// Esta funcion muestra los resultados de forma corta.
// No mostramos todo al tiro para que no se vea tan cargado.
function mostrarListaCompacta(actividades, busqueda) {
    resultados.innerHTML = "";
    document.body.classList.add("modo-resultados");

    if (actividades.length === 0) {
        mensaje.textContent = "No se encontraron actividades.";
        return;
    }

    mensaje.textContent = "Selecciona una actividad encontrada.";

    const lista = document.createElement("ul");

    actividades.forEach(function (actividad, indice) {
        const item = document.createElement("li");

        item.innerHTML = `
            <button type="button" data-indice="${indice}">
                ${destacar(actividad.nombre, busqueda)}
                — ${destacar(actividad.comuna, busqueda)}
                — ${escaparHTML(actividad.dia)}
            </button>
        `;

        lista.appendChild(item);
    });

    resultados.appendChild(lista);
}

// Esta funcion muestra el detalle de una actividad.
// Se usa cuando el usuario hace click en una actividad de la lista.
function mostrarDetalle(indice, busqueda) {
    const actividad = actividadesActuales[indice];

    // Si la actividad tiene foto, se muestra. Si no, dejamos la imagen por defecto.
    if (actividad.fotoUrl) {imagenActividad.src = actividad.fotoUrl;
    } else {imagenActividad.src = "/Califica.png";}

    resultados.innerHTML = `
        <article>
            <h2>${destacar(actividad.nombre, busqueda)}</h2>

            <p><strong>Miembro:</strong> ${escaparHTML(actividad.miembro)}</p>
            <p><strong>Días:</strong> ${escaparHTML(actividad.dia)}</p>
            <p><strong>Tipo:</strong> ${escaparHTML(actividad.tipo)}</p>
            <p><strong>Comuna:</strong> ${destacar(actividad.comuna, busqueda)}</p>
            <p><strong>Descripción:</strong> ${destacar(actividad.descripcion, busqueda)}</p>

            <p>
                <strong>Nota:</strong>
                <span id="nota-${actividad.id}">${escaparHTML(actividad.nota)}</span>
                (<span id="contador-${actividad.id}">${actividad.cantidadNotas}</span> evaluación(es))
            </p>

            <button type="button" id="boton-evaluar" data-id="${actividad.id}">
                Evaluar
            </button>

            <button type="button" id="boton-historial">
                Ver historial de notas
            </button>

            <button type="button" id="volver-lista">
                Volver a resultados
            </button>

            <div id="historial-${actividad.id}" class="caja-historial" style="display: none;">
                <h3>Historial de notas</h3>
                ${armarHistorial(actividad.historial)}
            </div>
        </article>
    `;

    mensaje.textContent = "Actividad seleccionada.";
}

// Esta funcion hace la busqueda de actividades.
// Es parecida a cuando usamos fetch para pedir datos para los graficos,
// solo que ahora pedimos actividades y no datos numericos.
async function buscarActividades() {
    const texto = input.value.trim();

    // Siguiendo la logica de Flask, antes de buscar revisamos si viene codigo raro.
    // Si viene algo raro, no hacemos fetch.
    if (tieneCodigoRaro(texto)) {
        mensaje.textContent = "Búsqueda inválida.";
        resultados.innerHTML = "";
        actividadesActuales = [];
        document.body.classList.remove("modo-resultados");
        imagenActividad.src = "/Califica.png";
        return;
    }

    // El enunciado pide buscar desde 3 caracteres.
    if (texto.length < 3) {
        mensaje.textContent = "Escribe al menos 3 caracteres.";
        resultados.innerHTML = "";
        actividadesActuales = [];
        document.body.classList.remove("modo-resultados");
        imagenActividad.src = "/Califica.png";
        return;
    }

    // Le pedimos a Spring las actividades que coinciden con el texto.
    const respuesta = await fetch("/api/actividades/buscar?q=" + encodeURIComponent(texto));
    const actividades = await respuesta.json();

    actividadesActuales = actividades;
    mostrarListaCompacta(actividades, texto);
}

// Cada vez que el usuario escribe, se vuelve a buscar.
input.addEventListener("input", buscarActividades);

// Aqui manejamos los clicks dentro de la zona de resultados.
// Lo hacemos asi porque los botones se crean despues con JavaScript.
resultados.addEventListener("click", function (evento) {
    const boton = evento.target.closest("button");
    if (boton === null) {return;}

    const texto = input.value.trim();

    // Si el boton tiene data-indice, significa que es una actividad de la lista.
    if (boton.dataset.indice !== undefined) {mostrarDetalle(Number(boton.dataset.indice), texto);}

    // Este boton muestra u oculta el historial de notas.
    if (boton.id === "boton-historial") {
        const caja = resultados.querySelector(".caja-historial");

        if (caja.style.display === "none") {caja.style.display = "block"; boton.textContent = "Ocultar historial";
        } else {caja.style.display = "none"; boton.textContent = "Ver historial de notas";}
    }

    // Aqui viene la parte de evaluar una actividad.
    if (boton.id === "boton-evaluar") {
        const actividadId = boton.dataset.id;

        // Si no viene usuarioId, no sabemos quien esta evaluando.
        if (usuarioId === null) {
            alert("No se pudo identificar al usuario. Entra desde la página de ingreso.");
            return;
        }

        const notaIngresada = prompt("Ingresa una nota entre 1 y 7:");
        if (notaIngresada === null) {return;}

        // Permitimos coma porque normalmente uno escribe 6,7.
        // Para mandarlo a Spring lo dejamos con punto: 6.7.
        const notaLimpia = notaIngresada.trim().replace(",", ".");

        // En la nota no usamos codigo raro porque no es texto libre:
        // tiene que cumplir este formato numerico.
        if (!/^[1-7](\.[0-9])?$/.test(notaLimpia)) {
            alert("La nota debe estar entre 1 y 7. Puedes usar decimal, por ejemplo 6,7.");
            return;
        }

        const notaNumero = Number(notaLimpia);
        if (notaNumero < 1 || notaNumero > 7) {
            alert("La nota debe estar entre 1 y 7.");
            return;
        }

        // Mandamos la nota a Spring para que la guarde en MySQL.
        fetch("/api/actividades/" + actividadId + "/notas", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nota: notaLimpia,
                usuarioId: usuarioId
            })
        })
        .then(function(respuesta) {return respuesta.json();})
        .then(function(datos) {
            if (datos.ok === false) {
                alert(datos.mensaje);
                return;
            }

            // Actualizamos la nota y el contador sin recargar la pagina.
            document.getElementById("nota-" + actividadId).textContent = datos.nota;
            document.getElementById("contador-" + actividadId).textContent = datos.cantidadNotas;

            // Tambien actualizamos el historial si la caja existe.
            const cajaHistorial = document.getElementById("historial-" + actividadId);
            if (cajaHistorial !== null) {
                cajaHistorial.innerHTML = `
                    <h3>Historial de notas</h3>
                    ${armarHistorial(datos.historial)}
                `;
            }

            // Actualizamos la copia local para que al volver al detalle no aparezca informacion vieja.
            for (let i = 0; i < actividadesActuales.length; i++) {
                if (String(actividadesActuales[i].id) === String(actividadId)) {
                    actividadesActuales[i].nota = datos.nota;
                    actividadesActuales[i].cantidadNotas = datos.cantidadNotas;
                    actividadesActuales[i].historial = datos.historial;
                }
            }

            alert("Evaluación guardada correctamente por " + datos.iniciales + ".");
        });
    }

    // Vuelve desde el detalle a la lista de resultados.
    if (boton.id === "volver-lista") {mostrarListaCompacta(actividadesActuales, texto);}
});
