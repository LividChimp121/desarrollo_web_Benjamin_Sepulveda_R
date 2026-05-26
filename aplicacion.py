from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#Creamos flask
app = Flask(__name__)

# Esto permite usar session (y así tener una memoria temporal para cada usuario que visita la página).
app.secret_key = "clave_simple_panorama_dcc"

# Ahora Flask se conecta a MySQL usando SQLAlchemy. La URI tiene este formato pedido:
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2"

#conectamos Flask con SQLAlchemy para poder usar la base de datos desde Python.
db = SQLAlchemy(app)

#creamos las tablas que vamos a usar en el proyecto. Estas tablas reflejan las tablas del SQL del profe, pero con algunos campos extra que mi proyecto necesita y que igual están en el sql. Si el campo ya existe, no lo vuelve a crear, así que no hay riesgo de perder datos.
class Miembro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    # En el SQL del profe la columna se llama email pero yo hice todo con el nombre correo, así que lo nombreo 
    # desde aquí antes de que explote
    correo = db.Column("email", db.String(120), nullable=False, unique=True)

    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)

    # MySQL no acepta fechas como 02-05-2026 en una columna DATETIME.
    # Por eso usamos el formato que MySQL sí entiende: 2026-05-02 00:00:00.
    fecha_registro = db.Column(db.String(100), nullable=False)

    # Esta columna viene del SQL del profe que la tengo que integrar.
    comuna_id = db.Column(db.Integer, nullable=False)

    actividades = db.relationship("Actividad", backref="miembro") 
    #Es para poder acceder a las actividades de un miembro con miembro.actividades, sin tener que hacer una consulta a la base de datos cada vez. Es como una relación directa entre las tablas Miembro y Actividad.


class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Columnas del SQL del profe.
    miembro_id = db.Column(db.Integer, db.ForeignKey("miembro.id"), nullable=False)
    dia = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.String(20), nullable=False)
    duracion = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)

    # Columnas que tenemos que poner de las actividades
    dias = db.Column(db.String(200), nullable=False)
    hora_fin = db.Column(db.String(20), nullable=False)
    lugar = db.Column(db.String(200), nullable=False)
    acompanado = db.Column(db.String(200), nullable=True)
    entretencion = db.Column(db.String(100), nullable=True)

    fotos = db.relationship("Foto", backref="actividad")
    # Una actividad puede tener muchos comentarios. Parte de la tarea 3 (nuevos)
    # Esto permite usar actividad.comentarios si lo necesitamos.
    comentarios = db.relationship("Comentario", backref="actividad")


#para guardar las fotos que suben los usuarios a cada actividad, con una relación de uno a muchos (una actividad puede tener varias fotos, pero cada foto pertenece a una sola actividad).
class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad.id"), nullable=False)

# Esta clase representa la tabla "comentario" de MySQL. (nuevo de la t3)
# Cada comentario pertenece a una actividad.
class Comentario(db.Model):
    #recordemos que _tablename_ es el nombre de la tabla en la base de datos, y las columnas son los campos que tiene cada comentario: id, nombre de quien comenta, texto del comentario, fecha del comentario, y el id de la actividad a la que pertenece el comentario.
    id = db.Column(db.Integer, primary_key=True)
    # Nombre de quien comenta
    nombre = db.Column(db.String(80), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.String(100), nullable=False)
    actividad_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad.id"),
        nullable=False)


#Devuelve la fecha y hora actual en formato MySQL. Esto es útil para registrar la fecha de registro de un nuevo miembro o la fecha de creación de una nueva actividad.
def obtener_fecha_actual():
    #Aqui no me sirvio datetimenow() directamente porque MySQL no acepta el formato que devuelve, así que tuve que formatearlo con strftime para que quede como 2026-05-02 00:00:00.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Comuna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, nullable=False)

def obtener_comuna_id(comuna):
    comuna_encontrada = Comuna.query.filter_by(nombre=comuna).first() #busca en la tabla comuna la comuna que tenga el nombre igual al que se le pasó a la función,
    #y devuelve el primer resultado que encuentra. Si no encuentra ninguna comuna con ese nombre, devuelve None.

    if comuna_encontrada is not None:
        return comuna_encontrada.id
    #y si es none, devuelve el id de la comuna santiago. (Es estricto rigor esta opción solo estaba
    #porque antes no le puse comunas a las tarjetas y me daba lata ponerles. ahora están actualizadas pero igual lo deje)
    return 130208

def obtener_comunas():
    # Traemos todas las comunas para mostrarlas como opciones en el formulario.
    return Comuna.query.order_by(Comuna.nombre).all()

#repetimos con regiones!
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)

def obtener_regiones():
    # Traemos todas las regiones para mostrarlas como opciones en el formulario.
    return Region.query.order_by(Region.nombre).all()

#Esto es porque para las pruebas solia borrar la base de datos, so, ahora pongo una función que asegura que las columnas que necesito estén en la base de datos, y si no están, las crea. Así no pierdo datos si borro la base de datos.
#dejando una base de datos minima :D
def cargar_datos_iniciales():

    if Miembro.query.count() > 0:
        return

    usuario_prueba = Miembro(
        tipo="estudiante",
        nombre="Usuario",
        apellido="Prueba",
        correo="usua@rio.com",
        telefono="+56900000000",
        password="Usuario123",
        region="Metropolitana",
        comuna="Santiago",
        fecha_registro="2026-05-02 00:00:00",
        comuna_id=130208
    )

    ana = Miembro(
        tipo="estudiante",
        nombre="Ana",
        apellido="Soto",
        correo="ana@uchile.cl",
        telefono="+56911111111",
        password="Ana123",
        region="Metropolitana",
        comuna="Providencia",
        fecha_registro="2026-05-03 00:00:00",
        comuna_id=130207
    )

    carlos = Miembro(
        tipo="profesor",
        nombre="Carlos",
        apellido="Pérez",
        correo="carlos@uchile.cl",
        telefono="+56922222222",
        password="Carlos123",
        region="Valparaíso",
        comuna="Viña del Mar",
        fecha_registro="2026-05-04 00:00:00",
        comuna_id=50503
    )

    maria = Miembro(
        tipo="estudiante",
        nombre="María",
        apellido="Díaz",
        correo="maria@uchile.cl",
        telefono="+56933333333",
        password="Maria123",
        region="Biobío",
        comuna="Concepcion",
        fecha_registro="2026-05-05 00:00:00",
        comuna_id=80205
    )

    javier = Miembro(
        tipo="estudiante",
        nombre="Javier",
        apellido="Muñoz",
        correo="javier@uchile.cl",
        telefono="+56944444444",
        password="Javier123",
        region="Metropolitana",
        comuna="Las Condes",
        fecha_registro="2026-05-06 00:00:00",
        comuna_id=130204
    )

    laura = Miembro(
        tipo="profesor",
        nombre="Laura",
        apellido="Gómez",
        correo="laura@uchile.cl",
        telefono="+56955555555",
        password="Laura123",
        region="Metropolitana",
        comuna="Ñuñoa",
        fecha_registro="2026-05-07 00:00:00",
        comuna_id=130210
    )

    diego = Miembro(
        tipo="funcionario",
        nombre="Diego",
        apellido="Salas",
        correo="diego@uchile.cl",
        telefono="+56966666666",
        password="Diego123",
        region="Metropolitana",
        comuna="Maipú",
        fecha_registro="2026-05-08 00:00:00",
        comuna_id=130212
    )

    db.session.add(usuario_prueba)
    db.session.add(ana)
    db.session.add(carlos)
    db.session.add(maria)
    db.session.add(javier)
    db.session.add(laura)
    db.session.add(diego)
    db.session.commit()

    actividades = [
        Actividad(
            nombre="Fútbol",
            dias="lunes",
            dia="lunes",
            hora_inicio="15:00",
            hora_fin="16:00",
            duracion="01:00",
            tipo="deporte",
            lugar="Cancha DCC",
            descripcion="Actividad deportiva en la cancha del DCC",
            acompanado="Con amigos",
            entretencion="Muy entretenida",
            miembro_id=usuario_prueba.id
        ),
        Actividad(
            nombre="Ajedrez",
            dias="lunes miercoles",
            dia="lunes",
            hora_inicio="18:00",
            hora_fin="20:00",
            duracion="02:00",
            tipo="recreación",
            lugar="Sala de estudio DCC",
            descripcion="Partidas de ajedrez con estudiantes",
            acompanado="Con amigos de la generación",
            entretencion="Muy entretenida",
            miembro_id=ana.id
        ),
        Actividad(
            nombre="Voleibol",
            dias="martes jueves",
            dia="martes",
            hora_inicio="17:00",
            hora_fin="19:00",
            duracion="02:00",
            tipo="deporte",
            lugar="Cancha Beauchef",
            descripcion="Voleibol en cancha Beauchef",
            acompanado="",
            entretencion="",
            miembro_id=carlos.id
        ),
        Actividad(
            nombre="Patinaje",
            dias="sabado domingo",
            dia="sábado",
            hora_inicio="10:00",
            hora_fin="12:00",
            duracion="02:00",
            tipo="deporte",
            lugar="Parque O'Higgins",
            descripcion="Patinaje recreativo en el parque",
            acompanado="",
            entretencion="Entretenida",
            miembro_id=maria.id
        ),
        Actividad(
            nombre="Basquetbol",
            dias="lunes viernes",
            dia="lunes",
            hora_inicio="19:00",
            hora_fin="21:00",
            duracion="02:00",
            tipo="deporte",
            lugar="Gimnasio Beauchef",
            descripcion="Basquetbol en el gimnasio",
            acompanado="Con compañeros del DCC",
            entretencion="",
            miembro_id=javier.id
        ),
        Actividad(
            nombre="Ajedrez",
            dias="miercoles",
            dia="miércoles",
            hora_inicio="16:00",
            hora_fin="18:00",
            duracion="02:00",
            tipo="recreación",
            lugar="Biblioteca Central",
            descripcion="Ajedrez en biblioteca",
            acompanado="",
            entretencion="",
            miembro_id=laura.id
        ),
        Actividad(
            nombre="Voleibol",
            dias="martes sabado",
            dia="martes",
            hora_inicio="18:30",
            hora_fin="20:00",
            duracion="01:30",
            tipo="deporte",
            lugar="Multicancha DCC",
            descripcion="Voleibol en multicancha DCC",
            acompanado="Con su familia",
            entretencion="Muy entretenida",
            miembro_id=diego.id
        )
    ]

    db.session.add_all(actividades)
    db.session.commit()




#Flask necesita activarse antes de usar la base de datos. Por eso, después de definir las tablas, ponemos esta línea que carga los datos iniciales dentro del contexto de la aplicación.
with app.app_context():
    # Cargamos datos iniciales. Si la base de datos ya tiene miembros, no hace nada. Si está vacía, agrega un usuario de prueba y algunas actividades para que no partamos de cero.
    cargar_datos_iniciales()


# Esta función es la que nos interesa para el index. Se inicia sin que el usuario haya tocado nada. Presenta los ultimos miembros y actividades
#y también le dice al HTML si tiene que abrir alguna ventana o mostrar algún mensaje, por ejemplo, si el usuario acaba de registrarse o iniciar sesión.
#(aparte de cargar los datos necesarios para los select de región y comuna).
def cargar_inicio(abrir="", login_error="", login_exito=""):
    ultimos_miembros = Miembro.query.order_by(Miembro.id.desc()).limit(5).all()
    ultimas_actividades = Actividad.query.order_by(Actividad.id.desc()).limit(5).all()

    # para que el usuario pueda elegir desde una lista y no escribir cualquier cosa, pero eso está en index, así que debemos pasarle los datos desde las tablas.
    regiones = obtener_regiones()
    comunas = obtener_comunas()

    return render_template(
        "index.html",
        ultimos_miembros=ultimos_miembros,
        ultimas_actividades=ultimas_actividades,
        regiones=regiones,
        comunas=comunas,
        abrir=abrir,
        login_error=login_error,
        login_exito=login_exito)


#Es bien probable que existan librerias que defiendan cosas maliciosas
#Sin embargo para no complicar, vamos a hacer una función simple que revise si el texto tiene algunos caracteres que podrían usarse para meter código malicioso,
#como <, >, {{, }}, {% o %}. Si el texto tiene alguno de esos caracteres, la función devuelve True, indicando que el texto es sospechoso. Si no tiene ninguno de esos caracteres, devuelve False.
def tiene_codigo_raro(texto):
    if texto is None:
        return True
    
    if "<" in texto or ">" in texto:
        return True
    if "{{" in texto or "}}" in texto:
        return True
    
    if "{%" in texto or "%}" in texto:
        return True
    return False

#Seguimos la lógica definida en index para validar registro, pero ahora validamos desde flask por si aca :D
def validar_registro_basico(nombre, apellido, correo, telefono, password, region, comuna):
    nombre = nombre.strip()
    apellido = apellido.strip()
    correo = correo.strip()
    telefono = telefono.strip()
    region = region.strip()
    comuna = comuna.strip()

    # Primero revisamos que no venga código metido en los campos.
    if tiene_codigo_raro(nombre):
        return "Nombre inválido."

    if tiene_codigo_raro(apellido):
        return "Apellido inválido."

    if tiene_codigo_raro(correo):
        return "Correo inválido."

    if tiene_codigo_raro(telefono):
        return "Teléfono inválido."

    if tiene_codigo_raro(password):
        return "Contraseña inválida."

    if tiene_codigo_raro(region):
        return "Región inválida."

    if tiene_codigo_raro(comuna):
        return "Comuna inválida."

    if len(nombre) < 3:
        return "Nombre inválido."

    if len(apellido) < 3:
        return "Apellido inválido."

    # Revisamos nombre y apellido con lo mismo que veníamos haciendo:
    # letras, espacios y tildes.
    letras_permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "

    for letra in nombre:
        if letra not in letras_permitidas:
            return "El nombre solo puede tener letras."

    for letra in apellido:
        if letra not in letras_permitidas:
            return "El apellido solo puede tener letras."

    if len(correo) < 5:
        return "Correo inválido."

    if "@" not in correo:
        return "Correo inválido."

    if "." not in correo:
        return "Correo inválido."

    # Dejamos el teléfono igual que en el formulario:
    # +56912345678
    if len(telefono) != 12:
        return "Teléfono inválido."

    if telefono[0] != "+":
        return "Teléfono inválido."

    if telefono[1] != "5":
        return "Teléfono inválido."

    if telefono[2] != "6":
        return "Teléfono inválido."

    for i in range(3, len(telefono)):
        if telefono[i] < "0" or telefono[i] > "9":
            return "Teléfono inválido."

    # Región y comuna vienen desde select, pero igual validamos que no estén vacías.
    if len(region) < 2:
        return "Región inválida."

    if len(comuna) < 2:
        return "Comuna inválida."

    if len(password) < 8:
        return "Contraseña muy corta."

    tiene_numero = False
    tiene_mayuscula = False

    for letra in password:
        if letra >= "0" and letra <= "9":
            tiene_numero = True

        if letra >= "A" and letra <= "Z":
            tiene_mayuscula = True

    if tiene_numero == False:
        return "La contraseña debe tener al menos un número."

    if tiene_mayuscula == False:
        return "La contraseña debe tener al menos una mayúscula."
    return ""

def validar_hora(hora):

    if len(hora) != 5:
        return False
    if hora[2] != ":":
        return False
    
    if hora[0] < "0" or hora[0] > "9":
        return False

    if hora[1] < "0" or hora[1] > "9":
        return False

    if hora[3] < "0" or hora[3] > "9":
        return False

    if hora[4] < "0" or hora[4] > "9":
        return False

    horas = int(hora[0] + hora[1])
    minutos = int(hora[3] + hora[4])

    if horas < 0 or horas > 23:
        return False

    if minutos < 0 or minutos > 59:
        return False

    return True


def hora_a_minutos(hora):
    horas = int(hora[0] + hora[1])
    minutos = int(hora[3] + hora[4])

    return horas * 60 + minutos


def calcular_duracion(hora_inicio, hora_fin):

    minutos_inicio = hora_a_minutos(hora_inicio)
    minutos_fin = hora_a_minutos(hora_fin)

    diferencia = minutos_fin - minutos_inicio

    horas = diferencia // 60
    minutos = diferencia % 60

    return str(horas).zfill(2) + ":" + str(minutos).zfill(2)


def validar_archivo_actividad(archivo):

    if archivo is None:
        return "Debes subir un archivo."

    if archivo.filename == "":
        return "Debes subir un archivo."

    nombre = archivo.filename.lower()

    # Para no complicarnos con video, dejamos imagen.
    # Así no pasa que después intentamos mostrar un mp4 dentro de un <img>.
    if nombre.endswith(".jpg") or nombre.endswith(".jpeg") or nombre.endswith(".png"):
        return ""
    return "El archivo debe ser jpg, jpeg o png."

# Validamos comentarios también en Flask. (tarea 3 nuevo)
# Aunque después validemos con el JavaScript, el servidor siempre debe revisar.
def validar_comentario(nombre, texto):
    nombre = nombre.strip()
    texto = texto.strip()

    if tiene_codigo_raro(nombre):
        return "Nombre inválido."

    if tiene_codigo_raro(texto):
        return "Texto inválido."

    if len(nombre) < 3:
        return "El nombre debe tener al menos 3 caracteres."

    if len(nombre) > 80:
        return "El nombre debe tener máximo 80 caracteres."

    if len(texto) < 5:
        return "El comentario debe tener al menos 5 caracteres."

    if len(texto) > 300:
        return "El comentario es demasiado largo."

    return ""


@app.route("/")
def inicio(): #Se modifico para poder abrir el formulario de ingreso o registro desde la URL, por ejemplo con /?abrir=ingreso o /?abrir=registro. 
    #Pero validando que esto que fue lo ultimo que hice en esta tarea, no se pueda usar para meter código raro, y que solo acepte los valores que de verdad usa el index para abrir las ventanas, que son ingreso y registro. Si el valor no es ninguno de esos, o si tiene código raro, no se abre ninguna ventana.
    abrir = request.args.get("abrir", "")

    # nos cuidamos de cosas raras como ya hacemos en otras rutas
    if tiene_codigo_raro(abrir):
        abrir = ""
    # solo aceptamos los valores que de verdad usa el index
    if abrir not in ["", "ingreso", "registro"]:
        abrir = ""
    return cargar_inicio(abrir=abrir)


@app.route("/ingreso")
def ingreso():

    # Si no hay sesión previa ingresada, no puede entrar a esta página, lo redirigimos al inicio con un mensaje de error.
    if "usuario_id" not in session:
        return cargar_inicio(
            abrir="ingreso",
            login_error="Debes iniciar sesión para registrar actividades."
        )

    actividades = Actividad.query.all()
    return render_template("ingreso.html", actividades=actividades)


@app.route("/miembros")
def miembros():

    miembros = Miembro.query.all()
    actividades = Actividad.query.all()

    # Si vengo desde ingreso y todavía hay sesión, vuelvo a ingreso.
    # Si no hay sesión, vuelvo al inicio.
    if request.args.get("volver") == "ingreso" and "usuario_id" in session: #Si la URL tiene el parámetro volver=ingreso y hay sesión, entonces
        volver_url = url_for("ingreso")
    else:
        volver_url = url_for("inicio")
    #Así nos aseguramos que si el usuario llegó a miembros desde ingreso, el botón de volver lo regresa a ingreso, pero si llegó a miembros desde cualquier otro lado o no tiene sesión, el botón de volver lo regresa al inicio.

    return render_template(
        "miembros.html",
        miembros=miembros,
        actividades=actividades,
        volver_url=volver_url)


@app.route("/datos/sesion-comentario")
def datos_sesion_comentario():
    if "usuario_id" not in session:
        return jsonify({"ok": False})
    miembro = Miembro.query.get(session["usuario_id"])
    if miembro is None:
        return jsonify({"ok": False})
    return jsonify({"ok": True, "nombre": miembro.nombre + " " + miembro.apellido})

@app.route("/graficos")
def graficos():

    miembros = Miembro.query.all()
    actividades = Actividad.query.all()

    # Misma lógica que miembros.
    if request.args.get("volver") == "ingreso" and "usuario_id" in session:
        volver_url = url_for("ingreso")
    else:
        volver_url = url_for("inicio")

    return render_template(
        "graficos.html",
        miembros=miembros,
        actividades=actividades,
        volver_url=volver_url
    )

# Ahora vienen las rutas para registrar miembros y actividades, y para iniciar sesión. Estas rutas reciben los datos de los formularios, 
# hacen validaciones similares a las de JavaScript pero ahora en el servidor, y luego interactúan con la base de datos para guardar los nuevos miembros o actividades, 
# o para verificar las credenciales de inicio de sesión.
@app.route("/registrar-estudiante", methods=["POST"])
def registrar_estudiante():

    nombre = request.form["nombre-estudiante"]
    apellido = request.form["apellido-estudiante"]
    correo = request.form["correo-estudiante"]
    telefono = request.form["telefono-estudiante"]
    region = request.form["region-estudiante"]
    comuna = request.form["comuna-estudiante"]
    password = request.form["password-estudiante"]

    # Validamos también en Flask.
    # Esto es necesario porque JavaScript se puede saltar.
    error = validar_registro_basico(
        nombre,
        apellido,
        correo,
        telefono,
        password,
        region,
        comuna
    )

    if error != "":
        return cargar_inicio(
            abrir="registro",
            login_error=error
        )

    correo_existente = Miembro.query.filter_by(correo=correo).first()

    if correo_existente is not None:
        return cargar_inicio(
            abrir="registro",
            login_error="Ese usuario ya existe. Usa otro correo."
        )

    nuevo_miembro = Miembro(
        tipo="estudiante",
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        correo=correo.strip(),
        telefono=telefono.strip(),
        password=password,
        region=region,
        comuna=comuna,
        fecha_registro=obtener_fecha_actual(),
        comuna_id=obtener_comuna_id(comuna)
    )

    db.session.add(nuevo_miembro)
    db.session.commit()

    return cargar_inicio(
        abrir="ingreso",
        login_exito="Registro exitoso. Ahora puedes iniciar sesión."
    )


@app.route("/registrar-profesor", methods=["POST"])
def registrar_profesor():

    nombre = request.form["nombre-profesor"]
    apellido = request.form["apellido-profesor"]
    correo = request.form["correo-profesor"]
    telefono = request.form["telefono-profesor"]
    region = request.form["region-profesor"]
    comuna = request.form["comuna-profesor"]
    password = request.form["password-profesor"]

    # Validamos también en Flask.
    error = validar_registro_basico(
        nombre,
        apellido,
        correo,
        telefono,
        password,
        region,
        comuna
    )

    if error != "":
        return cargar_inicio(
            abrir="registro",
            login_error=error
        )

    correo_existente = Miembro.query.filter_by(correo=correo).first()

    if correo_existente is not None:
        return cargar_inicio(
            abrir="registro",
            login_error="Ese usuario ya existe. Usa otro correo."
        )

    nuevo_miembro = Miembro(
        tipo="profesor",
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        correo=correo.strip(),
        telefono=telefono.strip(),
        password=password,
        region=region,
        comuna=comuna,
        fecha_registro=obtener_fecha_actual(),
        comuna_id=obtener_comuna_id(comuna)
    )

    db.session.add(nuevo_miembro)
    db.session.commit()

    return cargar_inicio(
        abrir="ingreso",
        login_exito="Registro exitoso. Ahora puedes iniciar sesión."
    )


@app.route("/registrar-funcionario", methods=["POST"])
def registrar_funcionario():

    nombre = request.form["nombre-funcionario"]
    apellido = request.form["apellido-funcionario"]
    correo = request.form["correo-funcionario"]
    telefono = request.form["telefono-funcionario"]
    region = request.form["region-funcionario"]
    comuna = request.form["comuna-funcionario"]
    password = request.form["password-funcionario"]

    # Validamos también en Flask.
    error = validar_registro_basico(
        nombre,
        apellido,
        correo,
        telefono,
        password,
        region,
        comuna
    )

    if error != "":
        return cargar_inicio(
            abrir="registro",
            login_error=error
        )

    correo_existente = Miembro.query.filter_by(correo=correo).first()

    if correo_existente is not None:
        return cargar_inicio(
            abrir="registro",
            login_error="Ese usuario ya existe. Usa otro correo."
        )

    nuevo_miembro = Miembro(
        tipo="funcionario",
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        correo=correo.strip(),
        telefono=telefono.strip(),
        password=password,
        region=region,
        comuna=comuna,
        fecha_registro=obtener_fecha_actual(),
        comuna_id=obtener_comuna_id(comuna)
    )

    db.session.add(nuevo_miembro)
    db.session.commit()

    return cargar_inicio(
        abrir="ingreso",
        login_exito="Registro exitoso. Ahora puedes iniciar sesión."
    )


@app.route("/login", methods=["POST"])
def login():

    cargo = request.form["cargo-ingreso"]
    correo = request.form["correo-ingreso"]
    password = request.form["password-ingreso"]

    # Validación simple también para el login.
    if tiene_codigo_raro(cargo):
        return cargar_inicio(
            abrir="ingreso",
            login_error="Ingreso inválido."
        )

    if tiene_codigo_raro(correo):
        return cargar_inicio(
            abrir="ingreso",
            login_error="Ingreso inválido."
        )

    if tiene_codigo_raro(password):
        return cargar_inicio(
            abrir="ingreso",
            login_error="Ingreso inválido."
        )

    miembro = Miembro.query.filter_by(
        tipo=cargo,
        correo=correo,
        password=password
    ).first()

    # Si el usuario no existe o la contraseña está mala.
    if miembro is None:
        return cargar_inicio(
            abrir="ingreso",
            login_error="Cargo, Usuario o contraseña incorrectas."
        )

    # Ahora guardamos sesión.
    session["usuario_id"] = miembro.id
    session["usuario_nombre"] = miembro.nombre
    session["usuario_tipo"] = miembro.tipo

    # Mostramos éxito en el formulario y luego el HTML redirige a /ingreso.
    return cargar_inicio(
        abrir="ingreso",
        login_exito="Ingreso exitoso."
    )


@app.route("/registrar-actividad", methods=["POST"])
def registrar_actividad():
    if "usuario_id" not in session:
        return cargar_inicio(
            abrir="ingreso",
            login_error="Debes iniciar sesión para registrar actividades."
        )

    nombre = request.form["nombre-actividad"]
    tipo = request.form["tipo-actividad"]
    dias = request.form.getlist("dias")
    hora_inicio = request.form["hora-inicio"]
    hora_fin = request.form["hora-fin"]
    lugar = request.form["lugar-actividad"]
    acompanado = request.form["acompanado"]
    entretencion = request.form["entretencion"]
    link_comunidad = request.form["link-comunidad"]
    link_actividad = request.form["link-actividad"]
    archivo = request.files["archivo-actividad"]

    # Validamos también en Flask, porque no basta solo Javascript.
    # La idea es hacer validaciones parecidas a las de JS, pero ahora en el servidor en caso que se logre bypasear.

    if tiene_codigo_raro(nombre):
        return redirect(url_for("ingreso"))

    if tiene_codigo_raro(lugar):
        return redirect(url_for("ingreso"))

    if tiene_codigo_raro(acompanado):
        return redirect(url_for("ingreso"))

    if tiene_codigo_raro(entretencion):
        return redirect(url_for("ingreso"))

    if tiene_codigo_raro(link_comunidad):
        return redirect(url_for("ingreso"))

    if tiene_codigo_raro(link_actividad):
        return redirect(url_for("ingreso"))

    if len(nombre.strip()) < 3:
        return redirect(url_for("ingreso"))

    if len(nombre.strip()) > 100:
        return redirect(url_for("ingreso"))

    if len(dias) == 0:
        return redirect(url_for("ingreso"))

    if validar_hora(hora_inicio) == False:
        return redirect(url_for("ingreso"))

    if validar_hora(hora_fin) == False:
        return redirect(url_for("ingreso"))

    if hora_a_minutos(hora_inicio) >= hora_a_minutos(hora_fin):
        return redirect(url_for("ingreso"))

    if len(lugar.strip()) < 3:
        return redirect(url_for("ingreso"))

    if len(lugar.strip()) > 200:
        return redirect(url_for("ingreso"))

    # Los campos opcionales igual tienen límite para que no metan textos gigantes.
    if len(acompanado.strip()) > 200:
        return redirect(url_for("ingreso"))

    if len(entretencion.strip()) > 100:
        return redirect(url_for("ingreso"))

    if len(link_comunidad.strip()) > 300:
        return redirect(url_for("ingreso"))

    if len(link_actividad.strip()) > 300:
        return redirect(url_for("ingreso"))

    if link_actividad.strip() == "":
        return redirect(url_for("ingreso"))

    if "http" not in link_actividad and "www." not in link_actividad:
        return redirect(url_for("ingreso"))

    error_archivo = validar_archivo_actividad(archivo)

    if error_archivo != "":
        return redirect(url_for("ingreso"))

    dias_texto = " ".join(dias)
    duracion = calcular_duracion(hora_inicio, hora_fin)

    nueva_actividad = Actividad(
        nombre=nombre.strip(),
        dias=dias_texto,
        dia=dias[0],
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        duracion=duracion,
        tipo=tipo,
        lugar=lugar.strip(),
        descripcion=nombre.strip(),
        acompanado=acompanado.strip(),
        entretencion=entretencion.strip(),
        miembro_id=session["usuario_id"]
    )

    db.session.add(nueva_actividad)
    db.session.commit()

    # Guardamos el archivo en static/archivos.
    # No confiamos completamente en el nombre original:
    # al menos cambiamos espacios y sacamos barras para que no se meta como ruta rara.
    nombre_archivo = archivo.filename
    nombre_archivo = nombre_archivo.replace(" ", "_")
    nombre_archivo = nombre_archivo.replace("/", "_")
    nombre_archivo = nombre_archivo.replace("\\", "_")

    ruta_archivo = os.path.join("static", "archivos", nombre_archivo)
    archivo.save(ruta_archivo)

    # Guardamos la foto en la tabla foto.
    nueva_foto = Foto(
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo,
        actividad_id=nueva_actividad.id
    )
    db.session.add(nueva_foto)
    db.session.commit()

    return redirect(url_for("ingreso"))


@app.route("/salir")
def salir():
    # Ahora cerramos la sesión completamente.
    session.clear()
    return redirect(url_for("inicio"))


# Página de detalle de una actividad.
@app.route("/actividad/<int:actividad_id>")
def detalle_actividad(actividad_id):
    actividad = Actividad.query.get(actividad_id)
    if actividad is None:
        abort(404)
    # Revisamos si existe sesión iniciada.
    usuario_logeado = "usuario_id" in session
    return render_template("actividad.html", actividad=actividad, usuario_logeado=usuario_logeado)

# Devuelve los comentarios de una actividad en formato JSON.
@app.route("/listar-comentarios/<int:actividad_id>")
def listar_comentarios(actividad_id):
    comentarios = (Comentario.query.filter_by(actividad_id=actividad_id).order_by(Comentario.id.desc()).all())
    lista = []
    for c in comentarios:
        lista.append({
            "id": c.id,
            "nombre": c.nombre,
            "texto": c.texto,
            "fecha": c.fecha})
    return jsonify(lista)

# Recibe un comentario desde fetch y lo guarda en MySQL. Luego devuelve el comentario con su ID y fecha asignados para mostrarlo en la página sin recargar.
# Revisamos que el id venga solo con números. Revisamos que la actividad exista. Revisamos que el texto no tenga cosas raras. Si todo está bien, guardamos el comentario y devolvemos su información.
# Si viene texto raro, devolvemos error. Si la actividad no existe, devolvemos error. Si el id no es un número, devolvemos error.
#aqui es importante que esta ruta sea POST porque estamos recibiendo datos para guardar, no solo para mostrar. Además, al devolver JSON, esta ruta se puede usar fácilmente con fetch desde JavaScript para agregar comentarios sin recargar la página.
@app.route("/agregar-comentario", methods=["POST"])
def agregar_comentario():

    nombre = request.form.get("nombre", "")
    texto = request.form.get("texto", "")
    actividad_id_str = request.form.get("actividad_id", "")

    # Primero revisamos que el id de la actividad sea un número.
    if actividad_id_str.isdigit() == False:
        return jsonify({"ok": False, "mensaje": "Actividad inválida."})

    actividad_id = int(actividad_id_str)
    # Ahora revisamos que esa actividad exista en la base de datos.
    actividad = Actividad.query.get(actividad_id)
    if actividad is None:
        return jsonify({"ok": False, "mensaje": "La actividad no existe."})
    # Validamos el nombre y el texto del comentario.
    error = validar_comentario(nombre, texto)

    if error != "":
        return jsonify({"ok": False, "mensaje": error})

    # Si todo está bien, guardamos el comentario.
    nuevo_comentario = Comentario(
        nombre=nombre.strip(),
        texto=texto.strip(),
        fecha=obtener_fecha_actual(),
        actividad_id=actividad_id
    )
    db.session.add(nuevo_comentario)
    db.session.commit()
    return jsonify({
        "ok": True,
        "comentario": {
            "id": nuevo_comentario.id,
            "nombre": nuevo_comentario.nombre,
            "texto": nuevo_comentario.texto,
            "fecha": nuevo_comentario.fecha
        }})

@app.route("/comentarios")
def comentarios():

    comentarios = Comentario.query.order_by(Comentario.id.desc()).all()

    # Revisamos si existe sesión iniciada para decidir
    # a dónde debe volver el usuario.
    usuario_logeado = "usuario_id" in session
    return render_template("comentarios.html", comentarios=comentarios, usuario_logeado=usuario_logeado)

# Aqui vienen las rutas para los gráficos. Estas rutas no devuelven HTML, sino datos en formato JSON que luego el JavaScript de la página de gráficos usa para mostrar los gráficos correspondientes. 
# Cada ruta hace una consulta a la base de datos, procesa los datos para contar lo que necesitamos, y luego devuelve un JSON con las etiquetas y valores para cada gráfico.
# Datos para gráfico de barras: miembros registrados por día.
@app.route("/datos/miembros-por-dia")
def datos_miembros_por_dia():
    miembros = Miembro.query.all()
    conteo_por_dia = {}
    for m in miembros:
        fecha_dia = m.fecha_registro.strftime("%Y-%m-%d")
        if fecha_dia not in conteo_por_dia:
            conteo_por_dia[fecha_dia] = 0
        conteo_por_dia[fecha_dia] = conteo_por_dia[fecha_dia] + 1
    fechas_ordenadas = sorted(conteo_por_dia.keys())

    etiquetas = []
    valores = []
    for fecha in fechas_ordenadas:
        etiquetas.append(fecha)
        valores.append(conteo_por_dia[fecha])
    return jsonify({"etiquetas": etiquetas, "valores": valores})


# Aqui es importante que esta ruta sea GET porque solo estamos pidiendo datos para mostrar, no estamos enviando datos para guardar. 
# Además, al devolver JSON, esta ruta se puede usar fácilmente con fetch desde JavaScript para obtener los datos y mostrar el gráfico sin recargar la página.
# Datos para gráfico de torta: actividades por tipo.
@app.route("/datos/actividades-por-tipo")
def datos_actividades_por_tipo():
    actividades = Actividad.query.all()
    conteo_por_tipo = {}
    for a in actividades:
        tipo = a.tipo
        if tipo is None or tipo == "":
            tipo = "sin tipo"
        if tipo not in conteo_por_tipo:
            conteo_por_tipo[tipo] = 0
        conteo_por_tipo[tipo] = conteo_por_tipo[tipo] + 1

    etiquetas = []
    valores = []
    for tipo in conteo_por_tipo:
        etiquetas.append(tipo)
        valores.append(conteo_por_tipo[tipo])

    return jsonify({"etiquetas": etiquetas, "valores": valores})


# Y luego de lo anterior, falta el gráfico de barras para actividades por comuna. La lógica es similar a la de actividades por tipo, pero ahora contamos por comuna. 
# Además, como cada actividad pertenece a un miembro, y cada miembro tiene una comuna, debemos revisar la comuna del miembro que registró cada actividad para hacer el conteo correcto.
# Datos para gráfico de barras: actividades por comuna.
@app.route("/datos/actividades-por-comuna")
def datos_actividades_por_comuna():
    actividades = Actividad.query.all()
    conteo_por_comuna = {}
    for a in actividades:
        miembro = a.miembro
        if miembro is None:
            continue
        comuna = miembro.comuna
        if comuna is None or comuna == "":
            comuna = "sin comuna"
        if comuna not in conteo_por_comuna:
            conteo_por_comuna[comuna] = 0

        conteo_por_comuna[comuna] = conteo_por_comuna[comuna] + 1

    #por ultimo ordenamos las comunas alfabéticamente para que el gráfico se vea mejor, y preparamos las etiquetas y valores para devolver el JSON.
    etiquetas = []
    valores = []
    for comuna in sorted(conteo_por_comuna.keys()):
        etiquetas.append(comuna)
        valores.append(conteo_por_comuna[comuna])

    return jsonify({"etiquetas": etiquetas, "valores": valores})

# La idea es mantener los graficos anteriores, osea miembros por día, actividades por tipo y actividades por comuna, pero agregar un gráfico de torta que muestre la proporción de miembros por tipo (estudiantes, profesores y funcionarios).
@app.route("/datos/miembros-por-tipo")
def datos_miembros_por_tipo():
    miembros = Miembro.query.all()

    estudiantes = 0
    profesores = 0
    funcionarios = 0

    for m in miembros:
        if m.tipo == "estudiante":
            estudiantes = estudiantes + 1
        elif m.tipo == "profesor":
            profesores = profesores + 1
        elif m.tipo == "funcionario":
            funcionarios = funcionarios + 1

    return jsonify({
        "estudiantes": estudiantes,
        "profesores": profesores,
        "funcionarios": funcionarios
    })

# Lo mismo, mantenemos los gráficos anteriores pero agregamos un gráfico de barras que muestre las actividades más realizadas, o sea, los nombres de actividades que se repiten más en la base de datos. Para esto, contamos cuántas veces aparece cada nombre de actividad, y luego devolvemos un JSON con las etiquetas (nombres de actividades) y valores (conteo de cada actividad) para mostrar el gráfico.
@app.route("/datos/actividades-mas-realizadas")
def datos_actividades_mas_realizadas():
    actividades = Actividad.query.all()
    conteo = {}

    for a in actividades:
        nombre = a.nombre.lower()

        if nombre not in conteo:
            conteo[nombre] = 0

        conteo[nombre] = conteo[nombre] + 1

    etiquetas = []
    valores = []

    for nombre in conteo:
        etiquetas.append(nombre)
        valores.append(conteo[nombre])

    return jsonify({
        "etiquetas": etiquetas,
        "valores": valores
    })

# Y por ultimo agregamos un gráfico de barras que muestre en qué días de la semana se realizan más actividades. Para esto, revisamos el campo "dias" de cada actividad, que puede tener varios días separados por espacios, y contamos cuántas actividades se realizan en cada día de la semana. Luego devolvemos un JSON con las etiquetas (días de la semana) y valores (conteo de actividades en cada día) para mostrar el gráfico.
@app.route("/datos/actividades-por-dia")
def datos_actividades_por_dia():
    actividades = Actividad.query.all()

    dias = {
        "lunes": 0,
        "martes": 0,
        "miercoles": 0,
        "jueves": 0,
        "viernes": 0,
        "sabado": 0,
        "domingo": 0
    }

    for a in actividades:
        dias_texto = a.dias.lower().split(" ")

        for dia in dias_texto:
            if dia == "lunes":
                dias["lunes"] = dias["lunes"] + 1
            elif dia == "martes":
                dias["martes"] = dias["martes"] + 1
            elif dia == "miercoles" or dia == "miércoles":
                dias["miercoles"] = dias["miercoles"] + 1
            elif dia == "jueves":
                dias["jueves"] = dias["jueves"] + 1
            elif dia == "viernes":
                dias["viernes"] = dias["viernes"] + 1
            elif dia == "sabado" or dia == "sábado":
                dias["sabado"] = dias["sabado"] + 1
            elif dia == "domingo":
                dias["domingo"] = dias["domingo"] + 1

    return jsonify(dias)


# Esto evita que el navegador guarde páginas con sesión iniciada.
# Tuve que investigar esto porque, después de cerrar sesión,
# si apretaba "atrás", el navegador seguía mostrando la página anterior.
# Con esta función le decimos al navegador que no guarde esas páginas en caché.
# Así, cuando el usuario vuelve atrás, el navegador le pide nuevamente la página al servidor
# y Flask detecta que ya no existe una sesión iniciada.
@app.after_request
def evitar_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(debug=True)

