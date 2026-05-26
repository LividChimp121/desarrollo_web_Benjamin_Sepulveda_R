# CC5002 - Tarea 3

Para ingresar/logear se hizo uno rapido :D

Tipo: estudiante
Correo: [usua@rio.com](mailto:usua@rio.com)
Contraseña: Usuario123
---

Para esta tarea se siguió trabajando sobre la base de la Tarea 2, pero ahora agregando principalmente comentarios dinámicos, gráficos conectados a Flask (que ya habiamos trabajado algo en ellos) y una vista más completa para las actividades.

La idea general fue mantener la estructura ya construida anteriormente, pero agregando nuevas funcionalidades reales conectadas a la base de datos y utilizando `fetch`, `JSON`, rutas Flask y gráficos dinámicos.

---

# Comentarios

Se agregó una sección de comentarios para cada actividad.

Ahora, cuando un usuario entra al detalle de una actividad, puede:

* ver comentarios existentes,
* agregar un comentario nuevo,
* y actualizar los comentarios sin recargar la página usando `fetch()`.

Cada comentario guarda:

* nombre del comentarista,
* texto,
* fecha,
* actividad asociada.

Los comentarios funcionan como comentarios públicos asociados a una actividad.

En un principio se pensó hacer que solo usuarios logeados pudieran comentar, porque igual es raro que cualquier persona pueda entrar y comentar libremente. Sin embargo, por cómo estaba planteada la tarea y por la lógica de “comunidad abierta”, finalmente se decidió dejar comentarios públicos.

De todas formas, sí se agregó una pequeña lógica opcional de “comentario destacado”:

* cualquier persona puede comentar normalmente,
* pero si el usuario tiene sesión iniciada, puede usar el botón:
  `Usar sesión iniciada para distintivo ⭐`
* en ese caso el comentario se publica usando automáticamente el nombre de la sesión y aparece con una estrella visual.

La idea era representar comentarios hechos por miembros reales del sistema sin bloquear completamente los comentarios públicos.

Además:

* si el usuario intenta usar el distintivo sin tener sesión iniciada,
* el sistema lo redirige automáticamente al login.


# Validaciones de comentarios

Como los comentarios quedaron abiertos al público, se tuvo cuidado con las validaciones.

Se valida tanto en Javascript como en Flask:

* que el nombre no venga vacío,
* que tenga mínimo 3 caracteres,
* máximo 80,
* que el comentario tenga al menos 5 caracteres,
* y que no se intenten ingresar cosas raras como:

```text
<script>
{{ }}
{% %}
<
>
```

Se implementó una función simple llamada `tiene_codigo_raro()` para detectar texto sospechoso antes de guardar datos en MySQL.

La idea no era construir un sistema de seguridad profesional, sino evitar inyecciones básicas y mostrar preocupación por validaciones backend además del frontend.

# Vista general de comentarios

También se agregó una página general de comentarios.

Ahora existen dos formas de ver comentarios:

* entrando al detalle de una actividad,
* o entrando a `/comentarios`.

Desde esa vista general:

* se pueden revisar todos los comentarios del sistema,
* ver a qué actividad pertenecen,
* y entrar directamente al detalle correspondiente.

Esto no era estrictamente obligatorio, pero se agregó porque dejar todos los comentarios escondidos dentro de las actividades se sentía poco natural.

# Vista detalle de actividad

Ahora cada actividad tiene su propia página.

Antes las actividades solo podían verse desde la lista de miembros, pero ahora existe:

```text
/actividad/<id>
```

En esta vista se muestran:

* datos completos de la actividad,
* imagen asociada,
* comentarios,
* formulario de comentarios.

Además, desde la portada se puede entrar directamente a las últimas actividades registradas sin tener que pasar obligatoriamente por miembros.

# Gráficos

Se implementaron los gráficos pedidos utilizando:

* Flask,
* `fetch`,
* rutas JSON,
* `jsonify()`,
* Chart.js.

Los gráficos principales son:

* miembros registrados por día,
* actividades por tipo,
* actividades por comuna.

Cada gráfico obtiene sus datos desde rutas Flask que consultan la base de datos y devuelven JSON.

Luego Javascript utiliza `fetch()` para pedir esos datos y Chart.js para dibujar los gráficos dinámicamente en el navegador.

También se mantuvieron algunos gráficos adicionales que ya existían anteriormente, pero ahora adaptados para usar datos reales desde Flask y no datos escritos manualmente en el HTML.

# Tipo de actividad

Se modificó el formulario de actividades para separar:

* nombre de actividad,
* tipo de actividad.

Antes el sistema solo guardaba nombres como:

* Fútbol,
* Ajedrez,
* Parapente.

Pero eso no sirve para un gráfico agrupado por categorías.

Entonces ahora:

* nombre: “Fútbol”
* tipo: “deporte”

o:

* nombre: “Ajedrez”
* tipo: “recreación”

Esto permite que el gráfico “actividades por tipo” tenga sentido real.

Además, el tipo ahora se selecciona mediante `<select>` y no escribiendo texto libre, para mantener consistencia en los datos.

# Consideración sobre grandes cantidades de datos

El gráfico de miembros registrados por día actualmente muestra cada fecha individualmente en el eje X, tal como lo pide el enunciado.

Sin embargo, se consideró que si el sistema creciera mucho, por ejemplo:

* registros diarios durante un año,
* o cientos de usuarios,

el gráfico podría volverse difícil de leer.

Una mejora futura sería:

* agrupar por semanas,
* meses,
* o rangos de tiempo dinámicos dependiendo de la cantidad de datos.

Por ahora se mantuvo por día porque es exactamente lo solicitado en la tarea.

# Manejo de sesión

Se siguió usando `session` de Flask para:

* mantener usuarios logeados,
* restringir acceso a `/ingreso`,
* registrar actividades,
* y distinguir comentarios con distintivo.

También se agregó lógica para:

* evitar que páginas privadas queden guardadas en caché,
* manejar correctamente botones de volver,
* y detectar automáticamente si el usuario tiene sesión activa.

# Validaciones frontend y backend

Se mantuvo la lógica de validar tanto en Javascript como en Flask.

La razón es que:

* Javascript puede saltarse fácilmente,
* pero Flask siempre debe revisar los datos antes de guardarlos.

Por eso prácticamente todos los formularios tienen:

* validaciones visuales en frontend,
* y validaciones reales en backend.

# Decisiones generales

Se intentó mantener el proyecto lo más entendible posible y sin sobrecomplicar demasiado la estructura.

Muchas cosas podrían hacerse usando librerías más avanzadas o separando más el proyecto, pero la idea fue mantener una lógica parecida a la de las tareas anteriores para:

* poder entender realmente el código,
* explicarlo fácilmente,
* y mantener coherencia con el trabajo ya construido.

También se prefirió priorizar:

* funcionamiento real,
* integración completa con Flask y MySQL,
* validaciones,
* y navegación consistente entre páginas.
