package com.example.myproject;

import jakarta.persistence.*;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "actividad_id")
    private Integer actividadId;

    private Double nota;

    @Column(name = "miembro_id")
    private Integer miembroId;

    private String iniciales;

    public Nota() {
    }

    public Nota(Integer actividadId, Double nota, Integer miembroId, String iniciales) {
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

    public Double getNota() {
        return nota;
    }

    public Integer getMiembroId() {
        return miembroId;
    }

    public String getIniciales() {
        return iniciales;
    }
}
