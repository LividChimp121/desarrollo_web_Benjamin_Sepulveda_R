package com.example.myproject;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FotoRepository extends JpaRepository<Foto, Integer> {

    Optional<Foto> findFirstByActividadId(Integer actividadId);
}
