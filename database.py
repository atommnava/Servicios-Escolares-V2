# Programa con el cual se va a diseñar la base de datos
import sqlite3

conexion = sqlite3.connect("BaseDatos")
cursorBD = conexion.cursor()  #  Cursor para ejecutar consultas


# Funcion que valida si la tabla ya existe en la base de datos o no
def existeTabla(nombreTabla):
    cursorBD.execute(
        """SELECT COUNT(name) FROM SQLITE_MASTER WHERE type ='table' AND name ='{}' """.format(
            nombreTabla
        )
    )
    if cursorBD.fetchone()[0] == 1:
        print("La tabla ya existe")
        return True
    else:
        cursorBD.execute(
            """ CREATE TABLE estudiante(clave_alumno INTEGER PRIMARY KEY, nombre STRING, apellido STRING, correo_electronico STRING, telefono INTEGER) """
        )
        return False
        print("La tabla no existe, se ha creado una nueva tabla")
