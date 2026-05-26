# CC5002 - Tarea 3

Para ingresar/logear se hizo uno rapido :D

Tipo: estudiante
Correo: [usua@rio.com](mailto:usua@rio.com)
Contraseña: Usuario123
---

Esta tarea la hice arriba de lo que ya tenía de la Tarea 2. Lo nuevo grande
son los comentarios dinámicos, los gráficos conectados a Flask con `fetch`
y JSON (que ya habiamos jugado algo con esto antes) y una vista de detalle
para cada actividad. Traté de no mover mucho lo que ya estaba y solo ir
sumando lo nuevo encima.

---

# Comentarios

Cada actividad ahora tiene su sección de comentarios. Cuando entras al
detalle podés ver los que ya están, agregar uno nuevo y que aparezca
al tiro sin recargar la página, usando `fetch()`.

Cada comentario guarda nombre, texto, fecha y la actividad a la que
pertenece.

Al principio pensé en dejar que solo los usuarios logeados pudieran
comentar, porque sí me hacía un poco de ruido que cualquiera entrara
y comentara, pero como la idea de la tarea apuntaba más a "comunidad
abierta", al final los dejé públicos.

Igual le di una vuelta extra: si el usuario tiene sesión iniciada,
puede apretar el botón `Usar sesión iniciada para distintivo ⭐` y el
comentario queda con su nombre real y con una estrella al lado, así
se distinguen de los anónimos. Si aprieta el botón sin tener sesión,
lo redirijo al login.

# Validaciones de comentarios

Como los dejé públicos, me preocupé un poco más con esto. Valido en
JS y también en Flask: que el nombre no venga vacío, mínimo 3 y máximo
80 caracteres, que el comentario tenga al menos 5, y que no metan cosas
raras tipo `<script>`, `{{ }}`, `{% %}`, `<` o `>`.

Para lo último seguí utilizando una función super simple llamada `tiene_codigo_raro()`
que revisa si el texto trae alguno de esos pedazos. No pretende ser
seguridad seria, solo evitar lo más obvio antes de mandar el texto a
MySQL.

# Vista general de comentarios

Aparte del detalle de cada actividad, agregué una página `/comentarios`
que lista todos los del sistema, muestra a qué actividad pertenece cada
uno y deja entrar al detalle. No estaba en el enunciado, pero me daba
la impresión rara que los comentarios quedaran escondidos solo dentro
de cada actividad.

# Vista detalle de actividad

Antes a una actividad solo se podía llegar pasando por miembros. Ahora
hay una URL `/actividad/<id>` que muestra los datos completos, la imagen,
los comentarios y el formulario. También conecté las "últimas actividades"
del inicio para entrar directo al detalle desde la portada.

# Gráficos

Los gráficos los armé como pide el enunciado: Flask devuelve los datos
en JSON, JS los pide con `fetch` y Chart.js los dibuja. Los tres
obligatorios son miembros registrados por día (línea), actividades por
tipo (torta) y actividades por comuna (barras). Cada uno tiene su ruta
`/datos/...` en Flask que arma el JSON.

Aparte mantuve algunos gráficos extras que ya tenía de la Tarea 2,
pero adaptados para pedirle los datos a Flask en vez de tenerlos
escritos a mano en el HTML como antes.

# Tipo de actividad

Antes el formulario guardaba solo el nombre de la actividad (Fútbol,
Ajedrez, Parapente). El tema es que para el gráfico de "actividades por
tipo" eso no servía, porque no es lo mismo "Ajedrez" que "deporte".
Entonces ahora hay dos campos: nombre (ej. "Fútbol") y tipo (ej.
"deporte" o "recreación"). El tipo lo dejé como `<select>` en vez de
texto libre para que la gente no escriba "deportes" / "Deportes" /
"deporte " y se desordene la torta.

# Sobre el gráfico de miembros por día

Hoy pone cada fecha individual en el eje X, tal cual lo pide el
enunciado. Sé que si el sistema creciera mucho (un año de registros,
cientos de usuarios) quedaría ilegible y habría que agrupar por
semanas o meses, pero con los datos actuales se ve bien y la tarea
pide "por día", así que lo dejé así nomás.

# Manejo de sesión

Sigo usando `session` de Flask igual que antes para mantener al usuario
logeado, restringir `/ingreso`, registrar actividades y ahora también
para el distintivo de comentarios. También quedó puesto el
`@app.after_request` de cache que había investigado en la Tarea 2
porque tenía un bug con el botón "atrás" después de cerrar sesión.

# Validaciones frontend y backend

Como en las tareas anteriores, todo lo importante lo valido en los dos
lados: JS para darle feedback al usuario al tiro, Flask por si alguien
se salta el JS. Es un poco repetitivo escribir lo mismo dos veces pero
me quedo más tranquilo así.

# Decisiones generales

Traté de no complicarme y mantener el código en la misma línea de la
Tarea 2: todo dentro de `aplicacion.py`, validaciones explícitas en vez
de librerías, y sin meter framework extra aparte de Chart.js. 

---

# Notas finales

- Quedó dando vueltas `templates/graficos.T2.Copia.html`, que es una
  copia vieja del template de gráficos de la Tarea 2 que usé de respaldo
  mientras armaba la nueva versión con Chart.js. No se usa en ninguna
  ruta, lo dejo por si lo quieren revisar pero se puede borrar tranquilo.
- Dejé los SQL del proyecto cargados en `sql/` por si acaso, para tener
  respaldo de la base.
- Pueden haber inconsistencias con los datos bases que deje desde inclusive la tarea 1, pero no me preocupe mucho más porque es simplemente borrarlos y ya, preocupandome más de que datos nuevos y todo lo que entre a la base de datos sea consistente en adelante.