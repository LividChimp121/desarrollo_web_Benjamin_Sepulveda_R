package com.example.myproject;

import jakarta.persistence.*;

@Entity
@Table(name = "miembro")
public class Miembro {

    @Id
    private Integer id;

    private String nombre;

    private String apellido;

    private String comuna;

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public String getComuna() {
        return comuna;
    }
}
