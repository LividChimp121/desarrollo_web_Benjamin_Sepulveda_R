package com.example.myproject;

import jakarta.persistence.*;

// Tabla donde guardamos las evaluaciones.
@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "actividad_id")
    private Integer actividadId;

    private Integer nota;

    @Column(name = "miembro_id")
    private Integer miembroId;

    private String iniciales;

    public Nota() {
    }

    public Nota(Integer actividadId, Integer nota, Integer miembroId, String iniciales) {
        this.actividadId = actividadId;
        this.nota = nota;
        this.miembroId = miembroId;
        this.iniciales = iniciales;
    }

    public Integer getId() {
        return id;
    }

    public Integer getActividadId() {
        return actividadId;
    }

    public Integer getNota() {
        return nota;
    }

    public Integer getMiembroId() {
        return miembroId;
    }

    public String getIniciales() {
        return iniciales;
    }
}