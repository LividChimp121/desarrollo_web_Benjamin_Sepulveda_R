# CC5002 - Tarea 1

## Descripción del proyecto

La idea del sistema es poder registrar actividades que realizan miembros del DCC (estudiantes, profesores y funcionarios) y luego poder consultarlas, filtrarlas y ver algunos gráficos simples.

---

## Decisiones de diseño

Tal como dije arriba, hice html separados tratando cada etapa por separado. En un principio, el registro de cada tipo de persona pide cosas distintas que hay que tener ojo, como los estudiantes la matricula, o los profesores el departamento de trabajo entre otros.

Luego al ingresar es "importante" poner con que se ingresa, porque tiene un estilo al ingresar con profesor o con estudiante o funcionario. Esto en realidad no es evidente, solo cambia la bienvenida, pero lo hice dado el contexto de la tarea y con un guardado temporal del html (data) que tuve que averiguar.

Lo siguiente fue crear el filtro y las tarjetas. Estas tarjetas tienen información ejemplificada tipica que se espera de un input de alguien que entrega una actividad, reutilizando en todo momento botones clasicos (minecraft que use mucho) y otros formatos de diseño que le dan color. 

Tambien decir que como fue el avance de una tarea, se vera cambios notorios entre html en cuanto al uso del css o reglas de como pedir obligatorio, todo eso en la otra sección-

En resumen: Todo se conecto con los html, se hizo uso de 2 css, el primero que pensé en globalizarlo pero luego, dado que igual quería ir practicando, cree el segundo para la "segunda parte de la tarea", evidenciando siempre como se desarrollo el aprendizaje de la tarea, todo bien comentado con fin de poder aprender bien.

---
## Filtros y paginación

El listado permite:

* Filtrar por tipo de miembro
* Buscar por nombre, correo, actividad, etc.
* Actualizar en tiempo real mientras se escribe
* Mostrar resultados paginados

La paginación se genera dinámicamente según lo que quede después del filtro, osea, es una busqueda por texto según el item que quieras buscar. Por ejemplo, puedes poner que quieres buscar por correo y si pones "a" te enseña todas las tarjetas con correo que incluya la letra a. Esto es importante, no se hace viendo de izquierda a derecha sino con un include() basico que ve si está dentro del filtro. 

Esto con dos fines, uno que quizas no se recuerda o los correos tienen numeros o cosas distintas que pueden molestar al momento de hacer la busqueda, y otro, que diferencia dos tipos de filtro, el filtro clasico por tipo que es por alumno, profe o funcionario que te los diferencia y siempre se sobreaplica al filtro especifico, y el ultimo que filtra por texto con tal de hacerlo más rapido. SIENDO UNO QUIEN DA ORDEN A QUE QUIERE BUSCAR, pues el sentido de poner de A-Z igual estorpece la busqueda a mi parecer. 

Y por ultimo las tarjetas, que se guardan dentro solo para poder calcular al minuto cuantas tarjetas mostrar, como crear la paginización (cuantos botones crear o eliminar según filtro) y así. 
---
## A tener en cuenta

Le pregunté al profesor/auxiliar sobre el ordenamiento porque no estaba seguro si mi forma de hacerlo era la correcta, pero no tuve una respuesta clara para esa parte. Por eso asumí que debía bastar con la justificación que di arriba, donde explico que se puede ordenar por distintos tipos y que el criterio se entiende según lo que el usuario escriba o seleccione.

Esto sí está implementado, solo hay que usar los filtros o escribir los valores para que se ordene según corresponda. Espero que con esa justificación sea suficiente y que esto no me baje la nota.

Y tambien como dije anteriormente, como esto fue un proceso de dias, se verá en los comentarios como fui avanzando o copiando y pegando partes anteriores, siempre comentando con un fin acádemico mio para priorizar el aprendizaje. Pero es eso, va progresivamente mejorando el trabajo :D

Otra cosa de ultima hora, antes tenía los <form> con <div>, esto porque como no iba a usar submit quería hacer los formularios y toda la mecanica con solo .js para aprender bien y todo eso. Lo arregle al final, según yo esta todo racional, pero por si acaso lo comento por si ven que está raro el codigo si es un form, o por ejemplo que todos los forms tienen botones con tipo botones y no con type submitt que tiene por defecto, y que eso en su minuto me rompio el codigo y casi lloré.

Pero debería estar todo bien :D
---

## Gráficos

Los gráficos los hice leyendo los datos desde las tarjetas. Esto porque encontraba muy básico mostrar un grafico generico o uno inventado sin aplicación propia (en las limitaciones de no disponer de una base de datos y con fe que esto sirva para las siguientes tareas :c)

Primero guardo la información en `localStorage` recorriendo las tarjetas con un for, y guardando:

* tipo
* actividad
* días

Que son las actividades obligatorias que la gente pone.
Luego en la página de gráficos leo eso, cuento con contadores y actualizo:

* barras por tipo
* barras por actividad
* barras por día
* gráfico de torta

---

## Validaciones

Las validaciones se hicieron con JavaScript sin nunuca ocupar required al ser muy basico y ya que me encargue de no poder mandar el formulario hasta validar todo :D
* campos obligatorios
* tipo de miembro
* actividad
* días seleccionados
* horario
* archivo obligatorio
* enlace
* datos de contacto
* etc

Cada validación está escrita en los comentarios de lo que opine que era lo mejor.
En los gmail no puse obligatoriamente el @uchile.com porque ni yo tengo el correo. Y tambien hay items no obligatorios pero que si los escribes tienen su correspondiente validación
---

## Cosas que agregué para que se viera mejor

* imagen rotativa al costado
* tarjetas con diseño simple
* botones minecraft
* gráficos dinamicos :D
* Y empeño :D

Intenté no complicar mucho el diseño y priorizar funcionalidad.
---
## Autor

Benjamin Sepúlveda