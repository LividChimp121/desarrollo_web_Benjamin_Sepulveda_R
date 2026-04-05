# CC5002 - Tarea 1

## Descripción del proyecto

La idea del sistema es poder registrar actividades que realizan miembros del DCC (estudiantes, profesores y funcionarios) y luego poder consultarlas, filtrarlas y ver algunos gráficos simples.

El flujo general del sistema permite registrarse según tipo de usuario, ingresar, registrar actividades, visualizar miembros, aplicar filtros, paginar resultados y finalmente ver gráficos simples.

---

## Decisiones de diseño

La aplicación se separó en distintos HTML para cada etapa del flujo. Esto permite mantener el código más ordenado y diferenciar claramente cada parte del sistema.

Cada tipo de usuario tiene formularios distintos, ya que requieren datos diferentes. Por ejemplo, los estudiantes deben ingresar matrícula y año, los profesores seleccionan departamento y los funcionarios indican su área de trabajo.

También se usaron dos archivos CSS. Uno principal y otro para la segunda parte del sistema. Esto se hizo porque el desarrollo fue progresivo y se quiso mantener esa separación para practicar.

El sistema se conecta entre páginas usando `localStorage`, lo que permite guardar información temporal como el tipo de usuario y los datos necesarios para los gráficos, esto lo vemos despúes el por qué lo usé.

---

## Formularios

Los formularios cambian según el tipo de persona. Todas las validaciones se hicieron con JavaScript, sin usar `required`, para tener control total del comportamiento y poder practicar.

Los campos obligatorios se validan al intentar enviar el formulario y se muestran mensajes indicando exactamente qué falta. Los campos opcionales pueden quedar vacíos, pero si el usuario escribe algo, se validan igualmente. En el segundo html (ingreso), los campos obligatorios se ven con asteriscos, pero de igual forma saltan los mensajes.

Inicialmente los formularios estaban hechos con `div`, pero luego se cambiaron a `form` para mejorar la semántica. Como no se utiliza submit, todos los botones son `type="button"` para evitar recargas de página y mantener el control con JavaScript.

---

## Filtros y paginación

El listado permite filtrar por tipo de miembro, buscar por nombre, correo, actividad u otros campos, actualizar en tiempo real mientras se escribe y mostrar resultados paginados.

Se entiende en esta tarea que lo que se pide en la tarea se cumple: Filtrado por tipo existe por si solo al poder filtrar por estudiante, profesores o funcionarios; pero tambien la busqueda por texto actualizado por los caracteres permite, al mismo usuario, ordenar y buscar según correo o nombre o todo, según como quiera buscar.

Este mismo filtro por texto funciona con `includes()`, permitiendo búsquedas parciales. Por ejemplo, si se busca por correo y se escribe una letra, se muestran todos los que contienen esa letra, siendo el usuario quien vea como prefiera buscar. Esto porque igual se pensó y si no te sabes el correo de un profesor, bueno pones correo y el nombre del profe, quizas tendrá numeros o una institución distinta, pero la busqueda será exitosa igual!

Entonces: Se combinan dos filtros, uno por tipo de miembro y otro por texto. Además la paginación se genera dinámicamente según los resultados del filtro, calculando cuántas tarjetas mostrar y cuántos botones crear al minuto y según el filtro, creando o borrando botones y actualizando en todo minuto.

---

## Gráficos

Con la idea de generar un gráfico dinamico y esperando que esto pueda (o no :c) servirme más adelante, hice uso de `localStorage` con la idea de guardar las tarjetas creadas en Miembros y usarlo en una especie de mini base de datos, simplemente cargando las tarjetas con el dataset.tipo de cada tipo, y con un for y contador, logrando calcular y generar gráficos que dependen de la experiencia de la pagina (Sentía muy básico crear graficos simples, como poner una barra o un grafico de torta inventado, aunque me esperaba que esto se tenía que hacer para la tarea)

Entonces:
Los gráficos se generan leyendo los datos desde las tarjetas. Para esto se guarda la información en `localStorage` recorriendo las tarjetas y almacenando tipo, actividad y días.

Luego la página de gráficos lee esos datos y genera gráficos de barras por tipo, gráficos por actividad, gráficos por días y un gráfico de torta. Esto permite que los gráficos dependan de los datos visibles y no sean estáticos.

---

## Validaciones

Las validaciones se hicieron completamente con JavaScript. 

No se obligó el uso de `@uchile.cl` en los correos para no restringir demasiado, aunque en el placeholder se les pide un correo institucional (sería la idea pero ni yo tengo el correo o lo uso). Los campos opcionales solo se validan si el usuario escribe algo.

---

## Extras agregados

No hay archivos separados .js. La decisión fue porque quería tener conectado cada html y luego las funciones que usaba para tener completa claridad del proceso de aprendizaje, no así .css que puede permitirse un poco de desorden.

Además, todo los archivos están comentados por mi persona con el fin de mostrar como fue el proceso de aprendizaje y creación del prototipo. Y tambien para mí, para ver como fue el proceso o acordarme de que iba tal cosa :D

Tambien para mejorar la visualización se agregaron imágenes rotativas decorativas, tarjetas con diseño simple, botones estilo minecraft, gráficos dinámicos, paginación y filtros en tiempo real.

---

## Autor

Benjamin Sepúlveda
