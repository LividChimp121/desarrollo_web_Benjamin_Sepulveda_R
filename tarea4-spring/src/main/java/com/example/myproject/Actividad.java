package com.example.myproject;

// Aqui haremos que Spring entienda la tabla actividad de MySQL.
// La idea es tratar una tabla SQL como una clase Java.
// Esto es parecido a lo que haciamos en Flask con class Actividad(db.Model).

// Importamos JPA, que es lo que permite conectar clases Java con tablas.
import jakarta.persistence.*;

// Con Entity le decimos a Spring que esta clase representa una tabla.
@Entity

// Con Table indicamos que la tabla real en MySQL se llama actividad.
@Table(name = "actividad")
public class Actividad {

    // id es la clave primaria de la tabla actividad.
    // Es lo mismo que en Flask era primary_key=True.
    @Id
    private Integer id;

    // Usamos la columna dias porque ahi queda guardada la lista completa.
    // En la base tambien existe dia, pero ese guarda solo un dia.
    @Column(name = "dias")
    private String dias;

    // Estos campos son columnas normales de la tabla actividad.
    private String tipo;
    private String nombre;
    private String descripcion;

    // Una actividad pertenece a un miembro.
    // Como un mismo miembro puede tener muchas actividades, usamos ManyToOne.
    @ManyToOne

    // La columna miembro_id es la que conecta actividad con miembro.
    // Es parecido al ForeignKey que usabamos en Flask.
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    // Desde el controller necesitamos leer el id de la actividad.
    public Integer getId() {
        return id;
    }

    // Devuelve los dias completos de la actividad.
    public String getDias() {
        return dias;
    }

    // Devuelve el tipo de actividad.
    public String getTipo() {
        return tipo;
    }

    // Devuelve el nombre de la actividad.
    public String getNombre() {
        return nombre;
    }

    // Devuelve la descripcion de la actividad.
    public String getDescripcion() {
        return descripcion;
    }

    // Devuelve el miembro que creo la actividad.
    // Con esto despues podemos sacar nombre, apellido o comuna.
    public Miembro getMiembro() {
        return miembro;
    }
}
