import sqlite3
from flask import Flask, g

# Conexión a la base de datos SQLite
conexion = sqlite3.connect("BaseDatos")
cursorBD = conexion.cursor()  # Cursor para ejecutar consultas


# Función que valida si la tabla ya existe en la base de datos
def existeTabla(nombreTabla):
    cursorBD.execute(
        """SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{}'""".format(
            nombreTabla
        )
    )
    if cursorBD.fetchone()[0] == 1:
        print("La tabla ya existe")
        return True
    else:
        cursorBD.execute(
            """CREATE TABLE estudiante (
                clave_alumno INTEGER PRIMARY KEY,
                nombre STRING,
                apellido STRING,
                correo_electronico STRING,
                telefono INTEGER
            )"""
        )
        print("La tabla no existe, se ha creado una nueva tabla")
        return False


# Verificar y crear la tabla si no existe
existeTabla("estudiante")


# Inserta un estudiante en la base de datos
def insertarEstudiante(nombre, apellido, correo, telefono):
    cursorBD.execute(
        """INSERT INTO estudiante (nombre, apellido, correo_electronico, telefono) VALUES (?, ?, ?, ?)""",
        (nombre, apellido, correo, telefono),
    )
    conexion.commit()
    print("Estudiante insertado correctamente")


# Ejemplos de inserción de estudiantes (descomentar para usar)
# insertarEstudiante("Atöm", "Nava", "atomnava@correo.uia.mx", 5551234567)
# insertarEstudiante("Daniel", "Nuño", "ing.picard.2024@correo.uia.mx", 5559876543)
# insertarEstudiante("Sofía", "Gómez", "sofiagomez@correo.uia.mx", 5554567890)


# Consulta todos los estudiantes en la base de datos
def consultarEstudiantes():
    cursorBD.execute("""SELECT * FROM estudiante""")
    listaEstudiantes = []
    for filaencontrada in cursorBD.fetchall():
        listaEstudiantes.append(filaencontrada)
    return listaEstudiantes


# Actualiza un estudiante en la base de datos
def actualizarEstudiante(clave_alumno, nombre, apellido, correo, telefono):
    cursorBD.execute(
        """UPDATE estudiante SET nombre = ?, apellido = ?, correo_electronico = ?, telefono = ? WHERE clave_alumno = ?""",
        (nombre, apellido, correo, telefono, clave_alumno),
    )
    conexion.commit()
    print("Estudiante actualizado correctamente")


# Borrar datos repetidos en la base de datos
def borrarDatosRepetidos():
    cursorBD.execute(
        """DELETE FROM estudiante WHERE clave_alumno NOT IN (
            SELECT MIN(clave_alumno) FROM estudiante GROUP BY nombre, apellido, correo_electronico, telefono
        )"""
    )
    conexion.commit()
    print("Datos repetidos borrados correctamente")


# Mostrar estudiantes en un formato tabular
def mostrarEstudiantes():
    estudiantes = consultarEstudiantes()
    print("Clave Alumno | Nombre | Apellido | Correo Electrónico | Teléfono")
    print("-" * 70)
    for estudiante in estudiantes:
        print(
            f"{estudiante[0]:<12} | {estudiante[1]:<6} | {estudiante[2]:<8} | {estudiante[3]:<20} | {estudiante[4]}"
        )


# Función para cerrar la conexión a la base de datos
def cerrarConexion():
    cursorBD.close()
    conexion.close()
    print("Conexión a la base de datos cerrada correctamente")


# Función para conectar la base de datos a una aplicación Flask
def conectarFlask(app):
    @app.before_request
    def before_request():
        g.conexion = sqlite3.connect("BaseDatos")
        g.cursorBD = g.conexion.cursor()

    @app.teardown_appcontext
    def teardown_db(exception):
        if hasattr(g, "conexion"):
            g.conexion.close()
            print("Conexión a la base de datos cerrada correctamente")

    return app


# Ejemplo de una aplicación Flask que usa la base de datos
app = Flask(__name__)
conectarFlask(app)


# Ruta de ejemplo para mostrar estudiantes
@app.route("/")
def index():
    g.cursorBD.execute("SELECT * FROM estudiante")
    estudiantes = g.cursorBD.fetchall()
    return f"Estudiantes en la base de datos: {estudiantes}"


# Ejecutar funciones de ejemplo
borrarDatosRepetidos()
mostrarEstudiantes()
cerrarConexion()

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
