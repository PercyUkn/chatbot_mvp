import mysql
import mysql.connector


def conexion(conexion_switch = 2):
    import mysql
    import mysql.connector
    if conexion_switch == 1:
        cnx = mysql.connector.connect(user='u650849267_chatbot', password='Chatbot1',
                                  host='45.93.101.1',
                                  database='u650849267_chatbot')
    elif conexion_switch == 2:
        cnx = mysql.connector.connect(user='chatbot_app', password='analitica_datos_UNI_E12',
                                  host='127.0.0.1',
                                  database='chatbot_admision')
    return cnx


# Insertar contexto en la BD
def inserta_contexto(contexto, conexion_switch=2):
    cnx = conexion(conexion_switch)
    cursor = cnx.cursor()
    # Borrando datos previos en la tabla
    cursor.execute("TRUNCATE TABLE hecho")

    # Creando lista de tuplas para bulk insert
    hechos = contexto.split("\n")
    value_data = []
    for i, j in enumerate(hechos):
        value_data.append((i, j))

    add_data = ("INSERT INTO hecho "
                "(id, hecho)"
                "VALUES (%s, %s)")
    cursor.executemany(add_data, value_data)
    print(f"{cursor.rowcount} registros insertados")

    cnx.commit()
    # cnx.rollback()
    cursor.close()
    cnx.close()

