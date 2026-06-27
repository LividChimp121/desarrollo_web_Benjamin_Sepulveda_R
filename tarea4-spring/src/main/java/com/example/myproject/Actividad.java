package com.example.myproject;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad")
public class Actividad {

    @Id
    private Integer id;

    @Column(name = "dias")
    private String dias;

    private String tipo;

    private String nombre;

    private String descripcion;

    @ManyToOne
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    public Integer getId() {
        return id;
    }

    public String getDias() {
        return dias;
    }

    public String getTipo() {
        return tipo;
    }

    public String getNombre() {
        return nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public Miembro getMiembro() {
        return miembro;
    }
}
