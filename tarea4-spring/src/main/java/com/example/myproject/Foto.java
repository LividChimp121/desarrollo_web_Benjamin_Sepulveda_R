package com.example.myproject;

import jakarta.persistence.*;

@Entity
@Table(name = "foto")
public class Foto {

    @Id
    private Integer id;

    @Column(name = "ruta_archivo")
    private String rutaArchivo;

    @Column(name = "nombre_archivo")
    private String nombreArchivo;

    @Column(name = "actividad_id")
    private Integer actividadId;

    public Integer getId() {
        return id;
    }

    public String getRutaArchivo() {
        return rutaArchivo;
    }

    public String getNombreArchivo() {
        return nombreArchivo;
    }

    public Integer getActividadId() {
        return actividadId;
    }
}
