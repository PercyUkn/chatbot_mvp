import random
import json

import torch

from model import NeuralNet

from train2 import init_model

from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


#contexto = "La película empieza con una escena de la guerra contra las máquinas tras el 'Día del Juicio Final' en el año 2029, donde Sarah Connor (Linda Hamilton) narra los sucesos relatados en la película anterior y de como Skynet, al fracasar su plan, ha decidido enfrentar a John siendo este todavía un niño. A continuación, hay un salto a la actualidad de 1995. Un Terminator T-800 (Schwarzenegger) llega desnudo a través de un portal en el tiempo y entra a una cafetería en las afueras de Los Ángeles para robar la ropa, el arma y la moto a un motociclista. En otra parte de la ciudad, otro individuo desnudo (Robert Patrick), se materializa y asesina a un policía para robar su uniforme y su auto patrulla. Ambos comienzan a buscar a John Connor (Edward Furlong), ahora con 10 años que vive en Los Ángeles con sus padres adoptivos. John es muy rebelde y constantemente desobedece a sus tutores, luego que su madre Sarah fuera arrestada después de intentar hacer explotar una fábrica de computadoras siendo internada en el hospital psiquiátrico de Pescadero, donde es atendida por el Doctor Silberman (Earl Boen)."
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
nlp = init_model();

def get_response(msg):

    response = nlp({'question': msg,'context':contexto_acerca_ocad})
    print(response)
    if response['score'] > 0.01: # Cuándo la probabilidad de haber respondido satisfactoriamente sea mayor a 10%
        return response['answer']
    else:
        return "No estoy muy seguro de mi respuesta"
