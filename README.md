# CC5002 - Tarea 4

Para ingresar/logear se hizo uno rapido :D

Tipo: estudiante
Correo: [usua@rio.com](mailto:usua@rio.com)
Contraseña: Usuario123

---

Esta tarea la hice arriba de lo que ya tenía de la Tarea 3. La idea fue no
rehacer toda la aplicación en Spring Boot, porque lo conversado en clases fue
que no había que migrar todo, sino implementar en Spring Boot lo nuevo de la
Tarea 4.

Por eso mantuve la aplicación principal en Flask y agregué una mini aplicación
Spring Boot dentro de la carpeta `tarea4-spring`, conectada a la misma base de
datos MySQL. La aplicación Flask sigue funcionando como antes, y desde la vista
de ingreso se puede entrar al buscador/evaluador hecho en Spring Boot.

---

# Cómo correr la aplicación

Hay que correr las dos aplicaciones al mismo tiempo.

## Flask

Desde la carpeta principal:

```bash
cd "/Users/benjas/Documents/App Web 04"
source ".venv/bin/activate"
python aplicacion.py
```

La aplicación principal queda en:

```text
http://127.0.0.1:5000/
```

## Spring Boot

Desde la carpeta de Spring:

```bash
cd "/Users/benjas/Documents/App Web 04/tarea4-spring"
mvn spring-boot:run
```

La parte nueva de la Tarea 4 queda en:

```text
http://localhost:8080/buscar
```

---

# Base de datos

La base de datos usada para esta tarea es:

```text
tarea_web_4
```

Decidí usar una base separada para no romper las tareas anteriores y para poder
probar la Tarea 4 con más tranquilidad.

Además de las tablas que ya venían de las tareas anteriores, agregué una tabla
nueva llamada `nota`, que guarda las evaluaciones de las actividades.

La tabla tiene, principalmente:

```text
id
actividad_id
nota
```

y después agregué también iniciales para dejar identificado de forma simple
quién evaluó.

---

# Decisión principal de implementación

La decisión más importante fue separar lo anterior de lo nuevo:

* Flask mantiene la aplicación principal.
* Spring Boot implementa el buscador y la evaluación de actividades.
* Ambas aplicaciones usan la misma base MySQL.
* Flask manda al usuario hacia Spring Boot desde la página de ingreso.
* Spring Boot permite volver a la página de ingreso de Flask.

Hice esto porque la tarea pedía usar Spring Boot, JPA y llamadas asíncronas,
pero no necesariamente rehacer todo lo que ya estaba listo en Flask.

---

# Buscador de actividades

En Spring Boot agregué una página `/buscar` con un único input de búsqueda.

Cuando el usuario escribe al menos 3 caracteres, se hace una llamada con
`fetch()` a un endpoint de Spring Boot:

```text
/api/actividades/buscar?q=...
```

La búsqueda revisa:

* nombre de la actividad,
* descripción,
* comuna del miembro asociado.

Los resultados muestran:

* miembro,
* días,
* tipo,
* comuna,
* nombre,
* descripción,
* nota promedio,
* cantidad de evaluaciones.

También dejé destacado en negrita el texto que coincide con la búsqueda, para
que se note qué fue lo que calzó.

---

# Selección de actividad

Al principio los resultados se mostraban como tarjetas completas, pero después
lo cambié para que se pareciera más a un buscador real.

Ahora se muestra primero una lista compacta de resultados. Cuando el usuario
selecciona una actividad, recién ahí se abre el detalle completo de esa
actividad.

Además, en el panel izquierdo se muestra una imagen. Si la actividad tiene foto
guardada en Flask, Spring Boot arma la ruta hacia esa foto usando la aplicación
Flask. Si no tiene foto, se muestra una imagen base de calificación.

---

# Evaluación de actividades

En el detalle de cada actividad agregué un botón `Evaluar`.

Al apretarlo, el usuario ingresa una nota entre 1 y 7. Esa nota se valida en el
frontend y también en Spring Boot.

Si la nota es válida, se envía con `fetch()` usando POST a:

```text
/api/actividades/{id}/notas
```

Spring Boot guarda la nota en la tabla `nota`, recalcula el promedio y devuelve
el nuevo promedio junto con la cantidad de evaluaciones.

La página actualiza la nota promedio y el contador sin recargar.

---

# Iniciales del usuario que evalúa

Como la evaluación se hace en Spring Boot pero la sesión real del usuario está
en Flask, tuve que buscar una forma simple de conectar ambas cosas.

La solución fue que, al entrar desde la página de ingreso de Flask, el botón
manda el `usuarioId` en la URL hacia Spring Boot. Con ese id, Spring puede buscar
al miembro en la base de datos y obtener sus iniciales.

Así la nota queda guardada con iniciales, sin pedirle al usuario que las escriba
a mano.

No quise intentar compartir la sesión completa entre Flask y Spring Boot porque
para esta tarea habría sido más enredado de lo necesario.

---

# Promedio de notas en comentarios

Aprovechando que las notas quedan guardadas en la misma base de datos, también
actualicé la vista de comentarios de Flask.

Ahora en `/comentarios`, cada comentario muestra la nota promedio de la actividad
a la que pertenece. Si la actividad todavía no tiene evaluaciones, aparece con
nota `-`.

Esto ayuda a conectar visualmente lo nuevo de la Tarea 4 con lo que ya existía
de la Tarea 3.

---

# Validaciones

La nota se valida en el frontend y en el backend.

En el frontend se revisa que sea un número entero entre 1 y 7 antes de mandarla
a Spring Boot.

En el backend se vuelve a validar porque no se puede confiar solo en JavaScript.
Si la nota no es válida, Spring devuelve un error y no guarda nada en la base.

También se valida que la actividad exista antes de guardar una nota asociada.

---

# JPA y modelos

En Spring Boot usé JPA para mapear las tablas principales que necesitaba:

* `Actividad`
* `Miembro`
* `Foto`
* `Nota`

También creé repositorios para consultar actividades, fotos, notas y miembros.

La búsqueda de actividades se hace con un repositorio que revisa nombre,
descripción y comuna usando una consulta con `LIKE`.

---

# Sobre los días de la actividad

Al principio Spring estaba leyendo un campo llamado `dia`, pero en la aplicación
Flask realmente se trabaja con `dias`, porque una actividad puede tener más de
un día.

Por eso corregí el modelo de Spring para leer la columna `dias` y mostrar todos
los días de la actividad, no solo el primero.

---

# Diseño

Intenté que la pantalla de evaluación no se viera como algo pegado a la fuerza.
Por eso agregué una vista con un panel de imagen y un panel de búsqueda.

También agregué un botón en la aplicación Flask para entrar a la parte de
calificación solamente después de haber ingresado a la app. No lo dejé en el
inicio público porque la idea era que estuviera dentro del flujo de usuario
logueado.

---

# Decisiones generales

Traté de mantener el estilo del proyecto original: código simple, validaciones
explícitas y sin meter demasiadas capas extras.

La Tarea 4 quedó como una integración entre Flask y Spring Boot. Flask sigue
siendo la app principal y Spring Boot se encarga de lo nuevo pedido: buscar y
evaluar actividades usando JPA y `fetch`.

No es una migración completa a Spring Boot, sino una extensión de la aplicación
existente.

---

# Notas finales

* Para que se vean las fotos reales de las actividades en Spring Boot, conviene
  tener Flask corriendo también, porque las imágenes están servidas desde
  `http://127.0.0.1:5000/static/...`.
* La carpeta `tarea4-spring` contiene todo lo nuevo de Spring Boot.
* Los SQL quedaron guardados en `sql/` como respaldo.
* Pueden quedar datos antiguos de tareas anteriores, pero la lógica nueva usa la
  misma base y las notas nuevas quedan guardadas correctamente.
