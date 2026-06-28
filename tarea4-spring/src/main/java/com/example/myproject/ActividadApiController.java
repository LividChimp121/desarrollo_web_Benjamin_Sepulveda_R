package com.example.myproject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// Logica principal de busqueda y evaluacion.
@RestController
public class ActividadApiController {

    private final ActividadRepository actividadRepository;
    private final NotaRepository notaRepository;
    private final FotoRepository fotoRepository;
    private final MiembroRepository miembroRepository;

    public ActividadApiController(
            ActividadRepository actividadRepository,
            NotaRepository notaRepository,
            FotoRepository fotoRepository,
            MiembroRepository miembroRepository) {
        this.actividadRepository = actividadRepository;
        this.notaRepository = notaRepository;
        this.fotoRepository = fotoRepository;
        this.miembroRepository = miembroRepository;
    }

    private boolean tieneCodigoRaro(String texto) {
        if (texto == null) {return true;}
        if (texto.contains("<") || texto.contains(">")) {return true;}
        if (texto.contains("{{") || texto.contains("}}")) {return true;}
        if (texto.contains("{%") || texto.contains("%}")) {return true;}
        return false;
    }

    // Promedio e historial de una actividad.
    private Map<String, Object> calcularNotas(Integer actividadId) {
        List<Nota> notas = notaRepository.findByActividadId(actividadId);

        Map<String, Object> datos = new HashMap<>();
        List<Map<String, Object>> historial = new ArrayList<>();

        String notaTexto = "-";
        int cantidadNotas = notas.size();

        if (cantidadNotas > 0) {
            int suma = 0;

            for (Nota nota : notas) {
                suma = suma + nota.getNota();

                Map<String, Object> item = new HashMap<>();
                item.put("nota", nota.getNota());

                if (nota.getIniciales() == null || nota.getIniciales().isBlank()) {item.put("iniciales", "-");
                } else {item.put("iniciales", nota.getIniciales());}

                historial.add(item);
            }

            double promedio = (double) suma / cantidadNotas;
            notaTexto = String.format("%.1f", promedio);
        }

        datos.put("nota", notaTexto);
        datos.put("cantidadNotas", cantidadNotas);
        datos.put("historial", historial);

        return datos;
    }

    @GetMapping("/api/actividades/buscar")
    public List<Map<String, Object>> buscarActividades(@RequestParam String q) {
        String texto = q.trim();

        if (tieneCodigoRaro(texto)) {return new ArrayList<>();}
        if (texto.length() < 3) {return new ArrayList<>();}

        List<Actividad> actividades = actividadRepository.buscarPorTexto(texto);
        List<Map<String, Object>> respuesta = new ArrayList<>();

        for (Actividad actividad : actividades) {
            Map<String, Object> datosNotas = calcularNotas(actividad.getId());

            String fotoUrl = "/Califica.png";
            var fotoEncontrada = fotoRepository.findFirstByActividadId(actividad.getId());

            if (fotoEncontrada.isPresent()) {
                Foto foto = fotoEncontrada.get();
                fotoUrl = "http://127.0.0.1:5000/" + foto.getRutaArchivo();
            }

            Map<String, Object> item = new HashMap<>();
            item.put("id", actividad.getId());
            item.put("miembro", actividad.getMiembro().getNombre() + " " + actividad.getMiembro().getApellido());
            item.put("dia", actividad.getDias());
            item.put("tipo", actividad.getTipo());
            item.put("comuna", actividad.getMiembro().getComuna());
            item.put("nombre", actividad.getNombre());
            item.put("descripcion", actividad.getDescripcion());
            item.put("nota", datosNotas.get("nota"));
            item.put("cantidadNotas", datosNotas.get("cantidadNotas"));
            item.put("historial", datosNotas.get("historial"));
            item.put("fotoUrl", fotoUrl);

            respuesta.add(item);
        }

        return respuesta;
    }

    @PostMapping("/api/actividades/{id}/notas")
    public ResponseEntity<Map<String, Object>> evaluarActividad(
            @PathVariable Integer id,
            @RequestBody Map<String, Object> datos) {

        Map<String, Object> respuesta = new HashMap<>();

        if (!actividadRepository.existsById(id)) {
            respuesta.put("ok", false);
            respuesta.put("mensaje", "La actividad no existe.");
            return ResponseEntity.badRequest().body(respuesta);
        }

        int notaNueva;

        // Se implementa logica de notas enteras.
        try {
            String notaTexto = datos.get("nota").toString().trim();

            if (!notaTexto.matches("[1-7]")) {
                respuesta.put("ok", false);
                respuesta.put("mensaje", "La nota debe ser un entero entre 1 y 7.");
                return ResponseEntity.badRequest().body(respuesta);
            }

            notaNueva = Integer.parseInt(notaTexto);
        } catch (Exception e) {
            respuesta.put("ok", false);
            respuesta.put("mensaje", "La nota debe ser un entero entre 1 y 7.");
            return ResponseEntity.badRequest().body(respuesta);
        }

        int usuarioId;

        // Spring recibe el usuario que venia desde Flask.
        try {
            usuarioId = Integer.parseInt(datos.get("usuarioId").toString());
        } catch (Exception e) {
            respuesta.put("ok", false);
            respuesta.put("mensaje", "No se pudo identificar al usuario.");
            return ResponseEntity.badRequest().body(respuesta);
        }

        var miembroEncontrado = miembroRepository.findById(usuarioId);

        if (miembroEncontrado.isEmpty()) {
            respuesta.put("ok", false);
            respuesta.put("mensaje", "No se encontró el usuario.");
            return ResponseEntity.badRequest().body(respuesta);
        }

        Miembro miembro = miembroEncontrado.get();

        String iniciales = "";
        iniciales = iniciales + miembro.getNombre().substring(0, 1).toUpperCase();
        iniciales = iniciales + ".";
        iniciales = iniciales + miembro.getApellido().substring(0, 1).toUpperCase();
        iniciales = iniciales + ".";

        Nota nota = new Nota(id, notaNueva, usuarioId, iniciales);
        notaRepository.save(nota);

        Map<String, Object> datosNotas = calcularNotas(id);

        respuesta.put("ok", true);
        respuesta.put("nota", datosNotas.get("nota"));
        respuesta.put("cantidadNotas", datosNotas.get("cantidadNotas"));
        respuesta.put("historial", datosNotas.get("historial"));
        respuesta.put("iniciales", iniciales);

        return ResponseEntity.ok(respuesta);
    }
}
