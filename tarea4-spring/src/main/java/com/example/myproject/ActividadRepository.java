package com.example.myproject;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    @Query("""
        SELECT a
        FROM Actividad a
        JOIN a.miembro m
        WHERE LOWER(a.nombre) LIKE LOWER(CONCAT('%', :texto, '%'))
           OR LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :texto, '%'))
           OR LOWER(m.comuna) LIKE LOWER(CONCAT('%', :texto, '%'))
        ORDER BY a.id DESC
    """)
    List<Actividad> buscarPorTexto(String texto);
}
