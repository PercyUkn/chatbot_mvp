"""Routes for parent Flask app."""
import flask
import mysql
from flask import render_template, request, jsonify
from flask import current_app as app
import os
#from chat2 import get_response


# Iniciar el modelo BERT / Cargar en memoria
def init_model():
    from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
    the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
    tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
    model = AutoModelForQuestionAnswering.from_pretrained(the_model)
    # TODO: Cargar contexto aquí
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return nlp;

contexto_total = """
La tasa de selectividad o admisión es de un ingresante por cada nueve postulantes. 
La Oficina de Central de Admisión (OCAD) inició sus actividades en 1980. 
La Universidad Nacional de Ingeniería (UNI) es una universidad pública peruana.
La OCAD se encarga de organizar, ejecutar y evaluar el proceso de ingreso a la Universidad, asegurando la incorporación de alumnos por sus méritos, que tengan las capacidades requeridas para seguir estudios universitarios.
El proceso automático de calificación de los exámenes se lleva a cabo en el Centro de Cómputo de la Oficina de Admisión bajo la supervisión de las autoridades de la universidad.
Las modalidades de admisión a la UNI son ordinario y extraordinario.
La carrera más demandada es ingeniería civil.
El proceso de admisión consta de tres exámenes que evalúan matemáticas, letras y física y química, cada examen dura tres horas.
El examen de admisión consta de tres partes que son evaluadas en tres fechas (lunes, miércoles y viernes) y tienen una duración de tres horas cada una.
Son 10 modalidades extraordinarias.
Las inscripciones para la modalidad IEN comienzan el lunes 18/10/2021 y terminan el jueves 25/11/2021. El examen de admisión 2022-I es el Lunes 01/03/2022.
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
"""

nlp = init_model();

# Obtener respuesta del modelo BERT
def get_response(msg):
    response = nlp({'question': msg, 'context': contexto_total})
    print(response)
    if response['score'] < 0.0001:  # Cuándo la probabilidad de haber respondido satisfactoriamente sea mayor a 10%
        response['answer'] = "No estoy muy seguro de mi respuesta"
    return response


def conexion():
    #cnx = mysql.connector.connect(user='u650849267_chatbot', password='Chatbot1',
    #                              host='45.93.101.1',
    #                              database='u650849267_chatbot')

    cnx = mysql.connector.connect(user='chatbot_app', password='analitica_datos_UNI_E12',
                                  host='127.0.0.1',
                                  database='chatbot_admision')
    return cnx


def inserta(json_data):
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

    cnx = conexion()
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
    inserta(datos_bd)
    message = {"answer": response}
    return jsonify(message)

# Cargar/servir recursos estáticos (imágenes para el dashboard)
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/assets')
@app.route('/static/assets/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

