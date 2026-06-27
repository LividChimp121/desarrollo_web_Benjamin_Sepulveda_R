const parametrosUrl = new URLSearchParams(window.location.search);
const usuarioId = parametrosUrl.get("usuarioId");

const input = document.getElementById("busqueda");
const mensaje = document.getElementById("mensaje");
const resultados = document.getElementById("resultados");
const imagenActividad = document.getElementById("imagen-actividad");

let actividadesActuales = [];

function escaparHTML(texto) {
    if (texto === null || texto === undefined) {
        return "";
    }

    return String(texto)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function destacar(texto, busqueda) {
    const textoSeguro = escaparHTML(texto);

    if (busqueda.length < 3) {
        return textoSeguro;
    }

    const busquedaEscapada = busqueda.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const expresion = new RegExp("(" + busquedaEscapada + ")", "gi");

    return textoSeguro.replace(expresion, "<strong>$1</strong>");
}

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

function mostrarDetalle(indice, busqueda) {
    const actividad = actividadesActuales[indice];

    if (actividad.fotoUrl) {
        imagenActividad.src = actividad.fotoUrl;
    } else {
        imagenActividad.src = "/Califica.png";
    }

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

async function buscarActividades() {
    const texto = input.value.trim();

    if (texto.length < 3) {
        mensaje.textContent = "Escribe al menos 3 caracteres.";
        resultados.innerHTML = "";
        actividadesActuales = [];
        document.body.classList.remove("modo-resultados");
        imagenActividad.src = "/Califica.png";
        return;
    }

    const respuesta = await fetch("/api/actividades/buscar?q=" + encodeURIComponent(texto));
    const actividades = await respuesta.json();

    actividadesActuales = actividades;
    mostrarListaCompacta(actividades, texto);
}

input.addEventListener("input", buscarActividades);

resultados.addEventListener("click", function (evento) {
    const boton = evento.target.closest("button");

    if (boton === null) {
        return;
    }

    const texto = input.value.trim();

    if (boton.dataset.indice !== undefined) {
        mostrarDetalle(Number(boton.dataset.indice), texto);
    }

    if (boton.id === "boton-historial") {
        const caja = resultados.querySelector(".caja-historial");

        if (caja.style.display === "none") {
            caja.style.display = "block";
            boton.textContent = "Ocultar historial";
        } else {
            caja.style.display = "none";
            boton.textContent = "Ver historial de notas";
        }
    }

    if (boton.id === "boton-evaluar") {
        const actividadId = boton.dataset.id;

        if (usuarioId === null) {
            alert("No se pudo identificar al usuario. Entra desde la página de ingreso.");
            return;
        }

        const notaIngresada = prompt("Ingresa una nota entre 1 y 7:");

        if (notaIngresada === null) {
            return;
        }

        const notaLimpia = notaIngresada.trim().replace(",", ".");

        if (!/^[1-7](\.[0-9])?$/.test(notaLimpia)) {
            alert("La nota debe estar entre 1 y 7. Puedes usar decimal, por ejemplo 6,7.");
            return;
        }

        const notaNumero = Number(notaLimpia);

        if (notaNumero < 1 || notaNumero > 7) {
            alert("La nota debe estar entre 1 y 7.");
            return;
        }

        fetch("/api/actividades/" + actividadId + "/notas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nota: notaLimpia,
                usuarioId: usuarioId
            })
        })
        .then(function(respuesta) {
            return respuesta.json();
        })
        .then(function(datos) {
            if (datos.ok === false) {
                alert(datos.mensaje);
                return;
            }

            document.getElementById("nota-" + actividadId).textContent = datos.nota;
            document.getElementById("contador-" + actividadId).textContent = datos.cantidadNotas;

            const cajaHistorial = document.getElementById("historial-" + actividadId);

            if (cajaHistorial !== null) {
                cajaHistorial.innerHTML = `
                    <h3>Historial de notas</h3>
                    ${armarHistorial(datos.historial)}
                `;
            }

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

    if (boton.id === "volver-lista") {
        mostrarListaCompacta(actividadesActuales, texto);
    }
});
