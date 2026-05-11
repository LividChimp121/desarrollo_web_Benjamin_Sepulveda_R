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

La lógica que se terminó implementando fue que para registrar actividades primero se debe iniciar sesión. Esto se entendió así porque en la portada aparece “Registrar miembro y actividades”, entonces se consideró más coherente que las actividades quedaran asociadas al usuario autenticado y no permitir registrar actividades “sueltas”, ya que eso complicaba después toda la relación entre miembros y actividades.

Inicialmente las actividades estaban directamente escritas en el HTML, pero después se decidió mover toda esa información a la base de datos para que realmente fueran dinámicas y poder trabajar correctamente con Flask y SQLAlchemy. Ahora las actividades se consultan desde Flask y se muestran usando ciclos `for` en los templates.

También al comienzo las actividades quedaban asociadas siempre al primer usuario de la base de datos porque se estaba usando `Miembro.query.first()`. Eso visualmente parecía funcionar, pero realmente estaba mal porque daba igual quién iniciara sesión. Después se cambió la lógica para trabajar usando `session["usuario_id"]`, de manera que cada actividad queda asociada al miembro que efectivamente inició sesión.

El login primero era solamente visual y dejaba acceder a páginas, pero no existía relación real entre usuario y actividad. Después se implementó el login conectado con SQLAlchemy, buscando correo y contraseña en la base de datos y guardando el usuario autenticado en sesión.

Se mantuvieron las validaciones que ya existían en JavaScript porque la tarea explícitamente lo pedía, pero además se agregaron validaciones en Flask del lado del servidor. Esto se hizo considerando entradas maliciosas y formularios enviados manualmente. También se agregaron límites de tamaño para archivos e imágenes para evitar subir archivos excesivamente grandes o incorrectos.

Además se incorporó la lógica de regiones y comunas usando la estructura entregada en los SQL de apoyo. La idea fue complementar los formularios originales sin cambiar demasiado la estructura que ya existía desde la tarea 1.

En las imágenes primero se consideró guardar archivos directamente en la base de datos, pero después se decidió guardar solamente la ruta/nombre del archivo y almacenar físicamente las imágenes dentro de `static/archivos`, porque simplificaba bastante el sistema y era más fácil mantener la lógica de Flask.

En el listado de miembros se implementó que al hacer click sobre una fila se pueda acceder al detalle del miembro y ver sus actividades asociadas. Además, si una actividad tiene imágenes asociadas, ahora también se pueden visualizar desde esa vista. La idea fue complementar el filtrado y navegación usando información obtenida directamente desde la base de datos.

La portada también se modificó para mostrar información dinámica obtenida desde SQLAlchemy. Se trabajó pensando en que el listado de miembros y actividades debía actualizarse automáticamente según la base de datos y no quedar fijo en HTML como estaba originalmente.

En los gráficos primero se utilizó `localStorage` porque era más rápido mientras todavía no estaba implementada toda la lógica backend. Después se decidió renovar esa parte para que los datos provinieran desde consultas reales usando SQLAlchemy, pensando en dejar toda la aplicación funcionando realmente conectada a la base de datos.

Durante el desarrollo existieron varios archivos SQL y bases distintas (`tarea.sql`, `comuna.sql`, `.db`, `appweb02.sql`) y llegó un momento donde ya no estaba claro cuál estaba usando Flask realmente. Entonces se decidió mantener solamente la base principal conectada al proyecto y eliminar archivos que ya no se estuvieran utilizando para evitar inconsistencias.

También se decidió reutilizar CSS entre páginas, especialmente `ingreso.css`, para mantener una estructura visual consistente y no duplicar estilos innecesariamente.

En general se intentó mantener el código relativamente simple. Varias veces se probaron soluciones más complejas, pero normalmente terminaban agregando demasiadas líneas o rompiendo partes que ya funcionaban. Por eso se prefirió modificar solamente lo necesario y mantener una estructura entendible considerando la entrevista individual de la tarea.
