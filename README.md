# CC5002 - Tarea 2

Para ingresar/logear se hizo uno rapido :D

Tipo: estudiante
Correo: [usua@rio.com](mailto:usua@rio.com)
Contraseña: Usuario123

De igual manera puedes crear una cuenta y logear desde allí.
No se permiten correos repetidos.


Recordar hablar que solo aceptare fotos, sacando la opcion de videos por la validación :D
Se decidió guardar físicamente los archivos en static/archivos y almacenar solo la ruta en la tabla foto para simplificar el manejo de archivos y mantener la base de datos más liviana.
---

La lógica que se terminó implementando fue que para registrar actividades primero se debe iniciar sesión (en la tarea se pide que esté el botón en el inicio, pero como no lo encuentro correcto y primero debes logear, aparece eso de si quieres registrar actividades logeate). Esto se entendió así porque en la portada aparece “Registrar miembro y actividades”, entonces se consideró más coherente que las actividades quedaran asociadas al usuario autenticado y no permitir registrar actividades “sueltas”, ya que eso complicaba después toda la relación entre miembros y actividades.

Se uso varios ciclos for para ir tomando los datos desde la base de datos :D

También al comienzo las actividades quedaban asociadas siempre al primer usuario de la base de datos porque se estaba usando `Miembro.query.first()`. Eso visualmente parecía funcionar, pero realmente estaba mal porque daba igual quién iniciara sesión. Después se cambió la lógica para trabajar usando `session["usuario_id"]`, de manera que cada actividad queda asociada al miembro que efectivamente inició sesión, como tambien, que al "salir" se cerrara completamente, inclusive si tratabas de entrar dando para atras a la pagina!

Tambien Se hizo las mismas validaciones entre flask y html en caso que html se bypaseara. A la vez, se incorporaron dos cosas más, que no se ingresará codigo malicioso entre otro tipo de maldad simplemente verificando los tipicas ortografias para iniciar código, como por ejemplo <> o {{}}. Es simple pero valido para no vulnerar.

El login busca tipo de cargo, mismo correo y contraseña para validarlo. El olvidar contraseña no lo implementé por simplicidad :D

Sé incorporó la lógica de regiones y comunas usando la estructura entregada en los SQL de apoyo. La idea fue complementar los formularios originales sin cambiar demasiado la estructura que ya existía desde la tarea 1.

En las imágenes primero se consideró guardar archivos directamente en la base de datos, pero después se decidió guardar solamente la ruta/nombre del archivo y almacenar físicamente las imágenes dentro de `static/archivos`, porque simplificaba bastante el sistema y era más fácil mantener la lógica de Flask. Observando tamaño del archivo y ya no se valida entregar videos por simplicidad de la validación!

Se crea una base de datos con datos falsos entre comillas de usuarios. Esto porque solia borrar varias veces las bases de datos para probar cosas que, luego como quedaban feas, las borraba (un usuario tipo ajdklsji@.com). Siempre se inicia con la base de datos normal, si ésta se borra, al menos tendrá tarjetas predefinidas!


En el listado de miembros se implementó que al hacer click sobre una fila se pueda acceder al detalle del miembro y ver sus actividades asociadas. Además, si una actividad tiene imágenes asociadas, ahora también se pueden visualizar desde esa vista. La idea fue complementar el filtrado y navegación usando información obtenida directamente desde la base de datos, con la misma lógica de busqueda que la tarea 1. Ahora bien, hay actividades que no tienen imagenes que son la de los usuarios de plantilla que dije arriba: me dio lata ponerles una imagen perdón :C
Pero luego como siempre se pide foto, en actividades nuevas habrán fotos! :D (además que se pueden acceder todasc las actividades por usuario al pincharlo)

La portada también se modificó para mostrar información dinámica obtenida desde SQLAlchemy. Se trabajó pensando en que el listado de miembros y actividades debía actualizarse automáticamente según la base de datos y no quedar fijo en HTML como estaba originalmente.

En los gráficos primero se utilizó `localStorage` porque era más rápido mientras todavía no estaba implementada toda la lógica backend. Después se decidió renovar esa parte para que los datos provinieran desde consultas reales usando SQLAlchemy, pensando en dejar toda la aplicación funcionando realmente conectada a la base de datos.

También se decidió reutilizar CSS entre páginas, especialmente `ingreso.css`, para mantener una estructura visual consistente y no duplicar estilos innecesariamente.

En general se intentó mantener el código relativamente simple. Varias veces se probaron soluciones más complejas, pero normalmente terminaban agregando demasiadas líneas o rompiendo partes que ya funcionaban. Por eso se prefirió modificar solamente lo necesario y mantener una estructura entendible considerando la entrevista individual de la tarea.
