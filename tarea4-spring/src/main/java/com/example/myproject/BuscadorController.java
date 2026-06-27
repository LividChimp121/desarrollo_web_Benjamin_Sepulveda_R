package com.example.myproject;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class BuscadorController {

    @GetMapping("/buscar")
    public String mostrarBuscador() {
        return "buscar";
    }
}
