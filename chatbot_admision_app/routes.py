"""Routes for parent Flask app."""
import flask
import mysql
import mysql.connector
from flask import render_template, request, jsonify
from flask import current_app as app
import os


# from chat2 import get_response


# Iniciar el modelo BERT / Cargar en memoria
def init_model():
    from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
    the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
    tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
    model = AutoModelForQuestionAnswering.from_pretrained(the_model)
    # TODO: Cargar contexto aquí
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return nlp;


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
def lee_contexto(conexion_switch=2):
    contexto = ""
    cnx = conexion(conexion_switch)
    cursor = cnx.cursor()

    # Leyendo los hechos de la BD
    cursor.execute("SELECT hecho FROM hecho")
    result_set = cursor.fetchall()
    for hecho in result_set:
        contexto += hecho[0]

    cursor.close()
    cnx.close()

    return contexto


def inserta(json_data,conexion_switch=2):
    # json_data = json.loads(json_text)

    preg = json_data['pregunta']
    resp_object = json_data["respuesta"]
    score = resp_object['score']
    start = resp_object['start']
    end = resp_object['end']
    answer = resp_object['answer']
    entendio = False
    # Umbral de aceptación
    if (score > 0.002):
        entendio = True

    cnx = conexion(conexion_switch)
    cursor = cnx.cursor()
    add_data = ("INSERT INTO pregunta "
                "(pregunta, entendio)"
                "VALUES (%s, %s)")
    value_data = (preg, entendio)
    cursor.execute(add_data, value_data)
    last_id = cursor.lastrowid

    add_data = ("INSERT INTO respuesta "
                "(score, start, end, answer, id_pregunta)"
                "VALUES (%s, %s, %s, %s, %s)")
    value_data = (score, start, end, answer, last_id)
    cursor.execute(add_data, value_data)
    cnx.commit()
    # cnx.rollback()
    cursor.close()
    cnx.close()


contexto = lee_contexto(1)
print(contexto)
# TODO: CARGAR A BASE DE DATOS
contexto_total = """La tasa de selectividad o admisión es de un ingresante por cada nueve postulantes. 
La Oficina de Central de Admisión (OCAD) inició sus actividades en 1980. 
La Universidad Nacional de Ingeniería (UNI) es una universidad pública peruana.
La OCAD se encarga de organizar, ejecutar y evaluar el proceso de ingreso a la Universidad, asegurando la incorporación de alumnos por sus méritos, que tengan las capacidades requeridas para seguir estudios universitarios.
El proceso automático de calificación de los exámenes se lleva a cabo en el Centro de Cómputo de la Oficina de Admisión bajo la supervisión de las autoridades de la universidad.
Las modalidades de admisión a la UNI son ordinario y extraordinario.
La carrera más demandada es ingeniería civil.
El proceso de admisión consta de tres exámenes que evalúan matemáticas, letras y física y química, cada examen dura tres horas.
El examen de admisión consta de tres partes que son evaluadas en tres fechas (lunes, miércoles y viernes) y tienen una duración de tres horas cada una.
Son 10 modalidades extraordinarias.
Las inscripciones para la modalidad IEN comienzan el lunes 18/10/2021 y terminan el jueves 25/11/2021. El examen de admisión general 2022-I es el Lunes 01/03/2022.
El prospecto cuesta S/ 90.00. El pago para dar o rendir el examen es de S/ 550.00.
Los pagos se realizarán en el banco BCP, agentes BCP o banca por internet BCP.
El teléfono para consultas es 981607508.
El correo para informes es informes@admisionuni.edu.pe.
La UNI ofrece 28 especialidades.
Se puede postular varias veces a la UNI, no hay límites para postular.
La UNI queda en Av. Tupac Amaru 210 Rímac
Hay 52 vacantes para Arquitectura.
Hay 25 vacantes para Física.
Hay 25 vacantes para Matemática.
Hay 25 vacantes para Química.
Hay 25 vacantes para Ingeniería física.
Hay 25 vacantes para Ciencias de la Computación.
Hay 28 vacantes para Ingeniería Sanitaria
Hay 28 vacantes para Ingeniería de Higiene.
Hay 28 vacantes para Ingeniería Ambiental.
Hay 126 vacantes para Ingeniería Civil.
Hay 39 vacantes para Ingeniería Económica.
Hay 37 vacantes para Ingeniería Estadística.
Hay 28 vacantes para Ingeniería Eléctrica.
Hay 28 vacantes para Ingeniería Electrónica.
Hay 28 vacantes para Ingeniería de Telecomunicaciones.
Hay 23 vacantes para Ingeniería Geológica.
Hay 30 vacantes para Ingeniería Metalúrgica.
Hay 27 vacantes para Ingeniería de Minas.
Hay 70 vacantes para Ingeniería Industrial.
Hay 70 vacantes para Ingeniería de Sistemas.
Hay 27 vacantes para Ingeniería Mecánica.
Hay 27 vacantes para Ingeniería Mecánica Eléctrica.
Hay 27 vacantes para Ingeniería Naval.
Hay 27 vacantes para Ingeniería Mecatrónica.
Hay 13 vacantes para Ingeniería Petroquímica.
Hay 13 vacantes para Ingeniería de Petróleo y Gas Natural.
Hay 31 vacantes para Ingeniería Química.
Hay 18 vacantes para Ingeniería Textil.
El orden de mérito en cada Especialidad se determina mediante la nota final que obtenga el postulante.
El examen de letras tiene 745 puntos.
El examen de matemáticas tiene 600 puntos.
El examen de física y química tiene 500 puntos.
Los puntos en total son 1845.
El puntaje mínimo para ingresar es 11.
Los resultados se publican en la página de la OCAD.
El Concurso de Admisión consiste en la evaluación de conocimientos, aptitudes, intereses vocacionales y la formación integral de los postulantes.
La UNI ofrece en total 754 vacantes.
El examen de IEN fue el Domingo 05/12/2022.
La tasa de ingreso para arquitectura es 8%.
La tasa de ingreso para física es 20.20%.
La tasa de ingreso para matemática es 27.60%.
La tasa de ingreso para química es 21.10%.
La tasa de ingreso para ingeniería física es 29.80%.
La tasa de ingreso para ciencia de la computación es 19.80%.
La tasa de ingreso para ingeniería sanitaria es 39.50%.
La tasa de ingreso para ingeniería de higiene y seguridad industrial es 46.70%.
La tasa de ingreso para ingeniería ambiental es 27%.
La tasa de ingreso para ingeniería civil es 14.80%.
La tasa de ingreso para ingeniería económica es 22.40%.
La tasa de ingreso para ingeniería estadística es 31.03%.
La tasa de ingreso para ingeniería eléctrica es 28.72%.
La tasa de ingreso para ingeniería electrónica es 17.30%.
La tasa de ingreso para ingeniería de telecomunicaciones es 25.47%.
La tasa de ingreso para ingeniería geológica es 30.26%.
La tasa de ingreso para ingeniería metalúrgica es 93.75%.
La tasa de ingreso para ingeniería de minas es 16.02%.
La tasa de ingreso para ingeniería industrial es 15.83%.
La tasa de ingreso para ingeniería de sistemas es 12.11%.
La tasa de ingreso para ingeniería mecánica es 19.07%.
La tasa de ingreso para ingeniería mecánica-eléctrica es 34.66%.
La tasa de ingreso para ingeniería naval es 80%.
La tasa de ingreso para ingeniería mecatrónica es 7.87%.
La tasa de ingreso para ingeniería petroquímica es 27.27%.
La tasa de ingreso para ingeniería de petróleo y gas natural es 29.41%.
La tasa de ingreso para ingeniería química es 19.56%.
La tasa de ingreso para ingeniería textil es 42.85%.
La nota mínima promedio para ingresar a Arquitectura es 11.573.
La nota mínima promedio para ingresar a Física es 12.135.
La nota mínima promedio para ingresar a Matemática es 11.004.
La nota mínima promedio para ingresar a Química es 12.183.
La nota mínima promedio para ingresar a Ingeniería Física es 11.199.
La nota mínima promedio para ingresar a Ciencia de la Computación es 11.337.
La nota mínima promedio para ingresar a Ingeniería Sanitaria es 11.127.
La nota mínima promedio para ingresar a Ingeniería de Higiene y Seguridad Industrial es 11.039.
La nota mínima promedio para ingresar a Ingeniería Ambiental es 13.146.
La nota mínima promedio para ingresar a Ingeniería Civil es 14.38.
La nota mínima promedio para ingresar a Ingeniería Económica es 11.331.
La nota mínima promedio para ingresar a Ingeniería Estadística es 11.001.
La nota mínima promedio para ingresar a Ingeniería Eléctrica es 13.023.
La nota mínima promedio para ingresar a Ingeniería Electrónica es 13.627.
La nota mínima promedio para ingresar a Ingeniería de Telecomunicaciones es 13.324.
La nota mínima promedio para ingresar a Ingeniería Geológica es 12.556.
La nota mínima promedio para ingresar a Ingeniería Metalúrgica es 12.115.
La nota mínima promedio para ingresar a Ingeniería de Minas es 12.478.
La nota mínima promedio para ingresar a Ingeniería Industrial es 14.419.
La nota mínima promedio para ingresar a Ingeniería de Sistemas es 13.654.
La nota mínima promedio para ingresar a Ingeniería Mecánica es 13.768.
La nota mínima promedio para ingresar a Ingeniería Mecánica-eléctrica es 13.109.
La nota mínima promedio para ingresar a Ingeniería Naval es 12.205.
La nota mínima promedio para ingresar a Ingeniería Mecatrónica es 14.304.
La nota mínima promedio para ingresar a Ingeniería Petroquímica es 11.011.
La nota mínima promedio para ingresar a Ingeniería de Petróleo y gas natural es 11.781.
La nota mínima promedio para ingresar a Ingeniería Química es 12.275.
La nota mínima promedio para ingresar a Ingeniería Textil es 11.186.
"""

nlp = init_model();


# Obtener respuesta del modelo BERT
def get_response(msg):
    response = nlp({'question': msg, 'context': contexto})
    print(response)
    if response['score'] < 0.0001:  # Cuándo la probabilidad de haber respondido satisfactoriamente sea mayor a 10%
        response['answer'] = "No estoy muy seguro de mi respuesta"
    return response


@app.get("/")
def index_get():
    return render_template("uni.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: Validar texto
    response_object = get_response(text)
    response = response_object['answer']

    # TODO: bd.save({'pregunta':text,'respuesta':response})
    datos_bd = {'pregunta': text, 'respuesta': response_object}
    inserta(datos_bd,2) # 1: BD en VPS/ 2: BD local
    message = {"answer": response}
    return jsonify(message)


# Cargar/servir recursos estáticos (imágenes para el dashboard)
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/assets')


@app.route('/static/assets/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)
