package com.example.myproject;

// Importamos JPA.
// Esto es lo que permite conectar una clase Java con una tabla de MySQL.
import jakarta.persistence.*;

// Esta clase representa la tabla actividad.
// Es lo mismo que haciamos en Flask con class Actividad(db.Model).
@Entity
@Table(name = "actividad")
public class Actividad {

    // Este campo es la clave primaria de la tabla.
    // Es lo mismo que en Flask era primary_key=True.
    @Id
    private Integer id;

    // Usamos dias porque ahi esta la lista completa de dias de la actividad.
    // En la base tambien existe dia, pero ese guarda solo un dia.
    @Column(name = "dias")
    private String dias;

    // Estos campos vienen directo de columnas de la tabla actividad.
    private String tipo;
    private String nombre;
    private String descripcion;

    // Una actividad pertenece a un miembro.
    // Muchas actividades pueden pertenecer al mismo miembro, por eso es ManyToOne.
    @ManyToOne

    // La columna miembro_id es la que conecta actividad con miembro.
    // Es parecido al ForeignKey que usabamos en Flask.
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    // Estos getters permiten leer los datos desde el controller.
    // Como los atributos son private, no los leemos directo.
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

    // Con esto podemos hacer actividad.getMiembro()
    // y desde ahi sacar nombre, apellido o comuna del miembro.
    public Miembro getMiembro() {
        return miembro;
    }
}
