# CC5002 - Tarea 1

## Descripción del proyecto

Este proyecto corresponde a un prototipo de sistema web para gestionar actividades de la comunidad del DCC.

La aplicación permite:

* Visualizar actividades disponibles
* Agregar nuevas actividades mediante un formulario
* Ver detalles de cada actividad
* Validar datos ingresados por el usuario

## Decisiones de diseño

* Se utilizó HTML5, CSS3 y JavaScript puro (sin frameworks), tal como lo solicita la tarea.
* Se organizó la interfaz en secciones claras: header, main y formularios emergentes.
* Se implementó una tabla para mostrar actividades de forma ordenada.

## Validaciones

Se implementaron validaciones en JavaScript para:

* Email con formato válido
* Número telefónico chileno (+569XXXXXXXX)
* Campos obligatorios como región, comuna y fechas
* Cantidad de imágenes (mínimo 1, máximo 5)

No se utilizó el atributo "required" como validación principal, sino solo como apoyo visual.

## Funcionalidades destacadas

* Ventana emergente para imágenes
* Formulario dinámico con selección de región/comuna
* Validación completa antes de enviar datos
* Confirmación antes de agregar actividad

## Observaciones

* No se almacena información, ya que es un prototipo
* Los datos de actividades están simulados en JavaScript

## Autor

Benjamin Sepúlveda



## Decisiones

Las primeras decisiones fue crear una imagen con IA para hacer ya la portada y los primeros botones. El tema es que en un principio estoy cree dos html que sean registro e ingreso pero eso no es una ventana emergente como debería ser de forma más limpia. 