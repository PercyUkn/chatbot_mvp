import random
import json

import torch

from model import NeuralNet

from train2 import init_model

# contexto = "La película empieza con una escena de la guerra contra las máquinas tras el 'Día del Juicio Final' en el año 2029, donde Sarah Connor (Linda Hamilton) narra los sucesos relatados en la película anterior y de como Skynet, al fracasar su plan, ha decidido enfrentar a John siendo este todavía un niño. A continuación, hay un salto a la actualidad de 1995. Un Terminator T-800 (Schwarzenegger) llega desnudo a través de un portal en el tiempo y entra a una cafetería en las afueras de Los Ángeles para robar la ropa, el arma y la moto a un motociclista. En otra parte de la ciudad, otro individuo desnudo (Robert Patrick), se materializa y asesina a un policía para robar su uniforme y su auto patrulla. Ambos comienzan a buscar a John Connor (Edward Furlong), ahora con 10 años que vive en Los Ángeles con sus padres adoptivos. John es muy rebelde y constantemente desobedece a sus tutores, luego que su madre Sarah fuera arrestada después de intentar hacer explotar una fábrica de computadoras siendo internada en el hospital psiquiátrico de Pescadero, donde es atendida por el Doctor Silberman (Earl Boen)."
contexto_acerca_ocad = """Las diversas actividades relacionadas con los concursos de admisión a la UNI están 
centralizadas en la Oficina Central de Admisión (OCAD) que inició sus actividades en 1980. La Oficina Central de 
Admisión es el órgano encargado de organizar, ejecutar y evaluar el proceso de ingreso a la Universidad, asegurando 
la incorporación de alumnos por sus méritos, que tengan las capacidades requeridas para seguir estudios 
universitarios. Sus actividades comprenden la formulación del presupuesto del concurso de admisión, la preparación 
del prospecto, la inscripción de los postulantes, la construcción y mantenimiento de un banco de preguntas, 
la elaboración de los exámenes de admisión y su aplicación, la preparación de los solucionarios de los exámenes 
aplicados, así como la entrega de la información y reportes de los ingresantes a cada una de las Facultades de la UNI 
y a la Oficina de Registros Académicos (ORCE). El proceso automático de calificación de los exámenes se lleva a cabo 
en el Centro de Cómputo de la Oficina de Admisión bajo la supervisión de las autoridades de la universidad. Parte 
importante de sus actividades está relacionada al análisis de los resultados obtenidos en cada concurso de admisión, 
con el objeto de mejorar el contenido de las pruebas aplicadas y poder así seleccionar a los jóvenes más idóneos para 
seguir estudios de acuerdo a las exigencias actuales en cada una de las 28 especialidades que ofrece la UNI. Las 
actividades de difusión de los estudios en la UNI en medio impreso, radial, televisivo y la participación en ferias 
vocacionales es otra de las tareas que la OCAD realiza permanentemente a nivel nacional. """

contexto_acerca_uni = """La Universidad Nacional de Ingeniería (siglas: UNI) es una universidad pública peruana 
ubicada en la ciudad de Lima. Fundada en 1876 como la Escuela de Ingenieros Civiles y de Minas, esta institución de 
carácter teórico-práctico tuvo al ingeniero polaco Eduardo de Habich como su primer director y formó parte de una 
iniciativa estatal que tenía por fin impulsar el desarrollo del Perú. Fue la primera escuela de ingenieros del país, 
posteriormente convertida en universidad en 1955. Como centro de educación politécnica está especializado en 
ingeniería, ciencias, y arquitectura. Su oferta académica está distribuida en once facultades que abarcan 28 carreras 
de pregrado, 57 programas de maestría y diez doctorados.Conocida por su rigurosa selectividad, la universidad cuenta 
con más de trece mil estudiantes y es considerada el principal centro de formación de ingenieros, científicos y 
arquitectos del Perú. Su campus principal se localiza en el distrito del Rímac y cuenta con un área de 66 hectáreas. """

contexto_admision = "La admisión a la universidad se realiza por concurso público dos veces al año en los meses de " \
                    "febrero y agosto. Entre las diferentes modalidades de ingreso dirigidas a los egresados de " \
                    "educación secundaria la más popular es el examen ordinario. Con el objetivo de seleccionar a los " \
                    "postulantes más capacitados para afrontar el alto nivel académico de los estudios de ingeniería, " \
                    "arquitectura y ciencias; la UNI tiene uno de los exámenes de admisión más exigentes del Perú.  " \
                    "Este examen consta de tres partes que son evaluadas en tres fechas (lunes, miércoles y viernes) " \
                    "y tienen una duración de tres horas cada una. La primera evalúa conocimientos de aptitud " \
                    "académica y humanidades, la segunda evalúa conocimientos de matemática y la tercera examina " \
                    "física y química. Los postulantes a la especialidad de Arquitectura deben rendir además una " \
                    "prueba de aptitud vocacional.16 En 2020 las carreras más demandadas fueron Ingeniería Civil, " \
                    "Arquitectura, Ingeniería de Sistemas, Ingeniería Mecatrónica e Ingeniería Industrial, " \
                    "estas en conjunto reunieron a más de la mitad del total de postulantes. Además de la exigencia " \
                    "académica, la competitividad del proceso de admisión a la UNI es muy alta. La tasa de " \
                    "selectividad ese mismo año fue de un ingresante por cada nueve postulantes. "

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


def get_response(msg):
    response = nlp({'question': msg, 'context': contexto_total})
    print(response)
    if response['score'] > 0.0001:  # Cuándo la probabilidad de haber respondido satisfactoriamente sea mayor a 10%
        return response['answer']
    else:
        return "No estoy muy seguro de mi respuesta"
