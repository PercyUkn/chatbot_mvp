from collections import Counter

import dash
from dash import html, callback
import os
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from flask import Flask, request
from flask_restful import Resource, Api
import math
import mysql.connector
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import dash.dependencies as dd
from io import BytesIO
import base64
import dash_bootstrap_components as dbc
from flask_login import current_user
import dash_defer_js_import as dji


def conexion(conexion_switch=2):
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


# Para servir imágenes estáticas

STATIC_PATH_DASHBOARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            '/static/css_dashboard/custom-style.css',
            '/static/css_dashboard/s1-plotly.css',
            # CDN de dash_bootstrap_components
        ],
        assets_folder=STATIC_PATH_DASHBOARD,
        # external_scripts=['/static/js_dashboard/99_custom-js.js']
    )

    dash_app._favicon = ("favicon.ico")
    # Tabs style
    tab_style = {
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#422729',
        'padding': '6px',
        'color': 'white',

    }

    tab_selected_style = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#422729',
        'color': 'white',
        'padding': '6px',
        'fontWeight': 'bold'
    }

    banner_style = {
        'border': '1px solid #d6d6d6',
        'fontSize': '20px'
    }

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                children=[
                    dbc.NavLink("Cerrar sesión", href="/logout", class_name="logout", id="logout_button"),
                    html.A(href="/logout")]
            ),
        ],
        brand="Equipo 12",
        brand_href="#",
        color="#422729",
        dark=True,
        style=banner_style
    )

    # Create Dash Layout
    dash_app.layout = html.Div(children=[

        # Navbar
        html.Div(children=[
            navbar
        ], className="row flex display"),
        html.Div(children=[

            # Cabecera
            html.Div(children=[
                html.Div(children=[

                    html.Img(src="/static/assets/logo-ocad.png",
                             title="Dashboard de películas",
                             style={
                                 "height": "100px",
                                 "width": "auto",
                                 'marginBottom': "25px"
                             }, id="logo_ocad"),

                ], className="one-third column"),

                html.Div([
                    html.Div([
                        html.H3("Dashboard - Chatbot admisión", style={"marginBottom": '0px', 'color': 'white'}),
                        html.H5('Equipo 12 - Analítica de datos', style={"marginBottom": '0px', 'color': 'white'})
                    ])
                ], className="one-third column", id="title"),

                html.Div([
                    html.Img(src="/static/assets/uni_admision.png",
                             title="OCAD UNI",
                             style={
                                 "height": "150px",
                                 "width": "auto",
                                 'marginBottom': "25px",
                                 "paddingLeft": "50px",
                                 "textAlign": "right"
                             }, id="uni")
                ], className="one-third column", id="title1")

            ], id="header", className="row flex display", style={'marginBottom': '25px'}), ]),

        # Tabs
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Chatbot', style=tab_style, selected_style=tab_selected_style, children=[

                    # Slider - Actualización de la base de datos
                    html.Div([
                        html.P('Seleccionar tiempo de actualización: ',
                               className="fix-label",
                               style={'color': 'white'}),
                        # Slider_update
                        html.Div([
                            dcc.Slider(
                                min=10,
                                max=40,
                                step=None,
                                value=5,
                                tooltip={"placement": "bottom", "always_visible": True},
                                id="interval_slider",
                                marks={
                                    10: '10 s',
                                    20: '20 s',
                                    30: '30 s',
                                    40: '40 s',
                                },
                                # className="dcc-compon",
                            )
                        ], className="card_container twelve columns"),

                    ], className="row flex display"),

                    # Chatbot (Pie y Barras)
                    html.Div([
                        # Pie días de uso
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_box,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="pie_dias_chatbot")
                        ], className="card_container six columns"),

                        # Histograma de uso
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_histogram,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="histograma_uso_chatbot")
                        ], className="card_container six columns"),
                        dcc.Interval(
                            id='interval-component',
                            interval=1 * 10000,  # Cada 10 segundos se actualiza automáticamente
                            n_intervals=0
                        )
                    ], className="row flex display"),

                    # Pie sobre eficacia y Line chart score
                    html.Div([
                        # Pie sobre eficacia
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_box,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="pie_efic_chatbot")
                        ], className="card_container six columns"),
                        html.Div([
                            dcc.Graph(
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="line_chart_score")
                        ], className="card_container six columns"),
                    ], className="row flex display"),

                    # KPI Score Promedio y KPI Eficacia
                    html.Div([
                        # KPI Score Promedio
                        html.Div([
                            # html.H5("Score de predicción promedio", style={"marginBottom": '0px', 'color': 'black'}),
                            dcc.Graph(id="mean_score_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container six columns", style={'textAlign': 'center'}),
                        # KPI Score Eficacia
                        html.Div([
                            # html.H5("Score de predicción promedio", style={"marginBottom": '0px', 'color': 'black'}),
                            dcc.Graph(id="eficacia_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container six columns", style={'textAlign': 'center'}),
                    ], className="row flex display"),

                    # KPI Costo, Vacantes, Fecha, Tema
                    html.Div([
                        # KPI Costo
                        html.Div([
                            dcc.Graph(id="costo_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container three columns", style={'textAlign': 'center'}),
                        # KPI Vacante
                        html.Div([
                            dcc.Graph(id="vacante_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container three columns", style={'textAlign': 'center'}),
                        # KPI Fecha
                        html.Div([
                            dcc.Graph(id="fecha_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container three columns", style={'textAlign': 'center'}),
                        # KPI Tema
                        html.Div([
                            dcc.Graph(id="tema_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container three columns", style={'textAlign': 'center'}),
                    ], className="row flex display"),

                    # Pie: Chatbot por categorías
                    html.Div([
                        # Pie del chatbot por categorías
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_box,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="fig_pie_categorias_chatbot")
                        ], className="card_container twelve columns"),
                    ], className="row flex display"),

                    # KPI Puntaje, General, Otros
                    html.Div([
                        # KPI Puntaje
                        html.Div([
                            dcc.Graph(id="puntaje_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container four columns", style={'textAlign': 'center'}),
                        # KPI General
                        html.Div([
                            dcc.Graph(id="general_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container four columns", style={'textAlign': 'center'}),
                        # KPI Otros
                        html.Div([
                            dcc.Graph(id="otros_kpi", config={'displayModeBar': False}, className="dcc-compon",
                                      style={'marginTop': '20px'}),
                        ], className="card_container four columns", style={'textAlign': 'center'}),
                    ], className="row flex display"),

                    # Pie: Chatbot por especialidad
                    html.Div([
                        # Pie del chatbot por especialidad
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_box,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="fig_pie_especialidad_chatbot")
                        ], className="card_container twelve columns"),
                    ], className="row flex display"),

                    # Nube de palabras
                    html.Div([
                        # Nube de palabras: Categorías
                        html.Div([

                            html.H5("Categorías más preguntadas", style={"marginBottom": '0px', 'color': 'black'}),
                            html.Img(title="Nube de palabras - Categorías", id="wordcloud_categorias"),

                        ], className="card_container six columns", style={'textAlign': 'center'}),
                        # Nube de palabras: Especialidades
                        html.Div([

                            html.H5("Especialidades más preguntadas", style={"marginBottom": '0px', 'color': 'black'}),
                            html.Img(title="Nube de palabras - Especialidades", id="wordcloud_especialidades"),

                        ], className="card_container six columns", style={'textAlign': 'center'}),

                    ], className="row flex display"),
                ]),
            ]),

        ]),
        html.Article(dji.Import(src="/static/js_dashboard/99_custom-js.js"))
    ], id="mainContainer", style={'display': 'flex', 'flexDirection': 'column'})

    dash_app.title = "Dashboard - Chatbot Admisión"
    # Inicializar callbacks
    init_callback(dash_app)

    return dash_app.server, dash_app


def init_callback(app):
    # Utilitarias
    def clasificador_pregunta(df):
        # Primera columna
        duracion_intent = ["dura", "toma tiempo", "tiempo toma"]
        costo_intent = ["cuesta", "precio", "costo", "pago", "cómo pago", "dónde pago", "banco", "cómo puedo pagar"]
        vacantes_intent = ["vacantes", "plazas", "espacios"]
        fechas_intent = ["cuándo", "cuando", "qué fecha", "fecha", "día", "dia", "cuándo será"]
        puntajes_intent = ["puntos", "puntaje", "cuánto se necesita", "nota", "tasa"]
        temas_examen_intent = ["temas", "que viene en", "que evalúa", "qué viene en", "qué evalúa"]
        general_info_intent = ["qué es la uni", "qué es", "qué significa", "qué hace", "que hace", "que es la ocad"]
        especialidades_intent = ["arquitectura", "física", "matemática", "química", "ingeniería física",
                                 "ciencia de la computación", "ingeniería sanitaria",
                                 "ingeniería de higiene y seguridad industrial", "ingeniería ambiental",
                                 "ingeniería civil", "ingeniería económica", "ingeniería estadística",
                                 "ingeniería eléctrica", "ingeniería electrónica", "ingeniería de telecomunicaciones",
                                 "ingeniería geológica", "ingeniería metalúrgica", "ingeniería de minas",
                                 "ingeniería industrial", "ingeniería de sistemas", "ingeniería mecánica",
                                 "ingeniería mecánica-eléctrica", "ingeniería naval", "ingeniería mecatrónica",
                                 "ingeniería petroquímica", "ingeniería de petróleo y gas natural",
                                 "ingeniería química", "ingeniería textil", "ing. ambiental", "ing. civil",
                                 "ing. de higiene y seguridad industrial", "ing. de minas",
                                 "ing. de petróleo y gas natural", "ing. de sistemas", "ing. de telecomunicaciones",
                                 "ing. económica", "ing. eléctrica", "ing. electrónica", "ing. estadística",
                                 "ing. física", "ing. geológica", "ing. industrial", "ing. mecánica",
                                 "ing. mecánica-eléctrica", "ing. mecatrónica", "ing. metalúrgica", "ing. naval",
                                 "ing. petroquímica", "ing. química", "ing. sanitaria", "ing. textil",
                                 "ingenieria ambiental", "ingenieria civil",
                                 "ingenieria de higiene y seguridad industrial", "ingenieria de minas",
                                 "ingenieria de petróleo y gas natural", "ingenieria de sistemas",
                                 "ingenieria de telecomunicaciones", "ingenieria económica", "ingenieria eléctrica",
                                 "ingenieria electrónica", "ingenieria estadística", "ingenieria física",
                                 "ingenieria geológica", "ingenieria industrial", "ingenieria mecánica",
                                 "ingenieria mecánica-eléctrica", "ingenieria mecatrónica", "ingenieria metalúrgica",
                                 "ingenieria naval", "ingenieria petroquímica", "ingenieria química",
                                 "ingenieria sanitaria", "ingenieria textil", "ambiental", "civil",
                                 "de higiene y seguridad industrial", "de minas", "de petróleo y gas natural",
                                 "de sistemas", "de telecomunicaciones", "económica", "eléctrica", "electrónica",
                                 "estadística", "física", "geológica", "industrial", "mecánica", "mecánica-eléctrica",
                                 "mecatrónica", "metalúrgica", "naval", "petroquímica", "química", "sanitaria",
                                 "textil", "higiene y seguridad industrial", "minas", "petróleo y gas natural",
                                 "sistemas"]

        # Segunda columna
        arquitectura_intent = ["arquitectura", "arqui"]
        computacion_intent = ["ciencia de la computación", "computación"]
        fisica_intent = ["física", "fisica"]
        ambiental_intent = ["ingeniería ambiental", "ambiental"]
        civil_intent = ["ingeniería civil", "civil"]
        higiene_intent = ["ingeniería de higiene y seguridad industrial", "higiene y seguridad industrial""higiene"]
        minas_intent = ["ingeniería de minas", "minas"]
        petroleo_intent = ["ingeniería de petróleo y gas natural", "petróleo y gas natural""petróleo""petroleo"]
        sistemas_intent = ["ingeniería de sistemas", "sistemas"]
        telecomunicaciones_intent = ["ingeniería de telecomunicaciones", "telecomunicaciones"]
        economica_intent = ["ingeniería económica", "económica"]
        electrica_intent = ["ingeniería eléctrica", "eléctrica"]
        electronica_intent = ["ingeniería electrónica", "electrónica"]
        estadistica_intent = ["ingeniería estadística", "estadística"]
        ing_fisica_intent = ["ingeniería física", "física"]
        geologica_intent = ["ingeniería geológica", "geológica"]
        industrial_intent = ["ingeniería industrial", "industrial"]
        mecanica_intent = ["ingeniería mecánica", "mecánica"]
        mecanica_electrica_intent = ["ingeniería mecánica-eléctrica", "mecánica-eléctrica"]
        mecatronica_intent = ["ingeniería mecatrónica", "mecatrónica"]
        metalurgica_intent = ["ingeniería metalúrgica", "metalúrgica"]
        naval_intent = ["ingeniería naval", "naval"]
        petroquimica_intent = ["ingeniería petroquímica", "petroquímica"]
        ing_quimica_intent = ["ingeniería química", "química"]
        sanitaria_intent = ["ingeniería sanitaria", "sanitaria"]
        textil_intent = ["ingeniería textil", "textil"]
        matematica_intent = ["matemática", ]
        quimica_intent = ["química", ]

        primera_columna_classifiers = [
            {"category": "Duración", "classifier": duracion_intent},
            {"category": "Costo", "classifier": costo_intent},
            {"category": "Vacantes", "classifier": vacantes_intent},
            {"category": "Fechas", "classifier": fechas_intent},
            {"category": "Puntaje", "classifier": puntajes_intent},
            {"category": "Temas", "classifier": temas_examen_intent},
            {"category": "Info general", "classifier": general_info_intent},
            {"category": "Especialidades", "classifier": especialidades_intent}
        ]

        segunda_columna_classifiers = [
            {"category": "Arquitectura", "classifier": arquitectura_intent},
            {"category": "Computacion", "classifier": computacion_intent},
            {"category": "Fisica", "classifier": fisica_intent},
            {"category": "Ingeniería ambiental", "classifier": ambiental_intent},
            {"category": "Ingeniería civil", "classifier": civil_intent},
            {"category": "Ingeniería de higiene", "classifier": higiene_intent},
            {"category": "Ingeniería de minas", "classifier": minas_intent},
            {"category": "Ingeniería de petróleo", "classifier": petroleo_intent},
            {"category": "Ingeniería de sistemas", "classifier": sistemas_intent},
            {"category": "Ingeniería de telecomunicaciones", "classifier": telecomunicaciones_intent},
            {"category": "Ingeniería de economica", "classifier": economica_intent},
            {"category": "Ingeniería eléctrica", "classifier": electrica_intent},
            {"category": "Ingeniería electrónica", "classifier": electronica_intent},
            {"category": "Ingeniería estadística", "classifier": estadistica_intent},
            {"category": "Ingeniería física", "classifier": ing_fisica_intent},
            {"category": "Ingeniería geológica", "classifier": geologica_intent},
            {"category": "Ingeniería industrial", "classifier": industrial_intent},
            {"category": "Ingeniería mecánica", "classifier": mecanica_intent},
            {"category": "Ingeniería mecánica_eléctrica", "classifier": mecanica_electrica_intent},
            {"category": "Ingeniería mecatrónica", "classifier": mecatronica_intent},
            {"category": "Ingeniería metalúrgica", "classifier": metalurgica_intent},
            {"category": "Ingeniería naval", "classifier": naval_intent},
            {"category": "Ingeniería petroquimica", "classifier": petroquimica_intent},
            {"category": "Ingeniería química", "classifier": ing_quimica_intent},
            {"category": "Ingeniería sanitaria", "classifier": sanitaria_intent},
            {"category": "Ingeniería textil", "classifier": textil_intent},
            {"category": "Matemática", "classifier": matematica_intent},
            {"category": "Quimica", "classifier": quimica_intent},
        ]

        preguntas = list(df['pregunta'])
        df['categoria'] = "Otros"
        df['especialidad'] = ""

        for i, pregunta in enumerate(preguntas):
            categoria_asignada = False
            for classifier in primera_columna_classifiers:
                for intent in classifier["classifier"]:
                    if intent in pregunta.lower():
                        category = classifier["category"]

                        if not category == "Especialidades" and not categoria_asignada:
                            df.iloc[i, 4] = category
                            categoria_asignada = True

                        if category == "Especialidades":
                            # Por qué especialidad pregunta?
                            for classifier_2 in segunda_columna_classifiers:
                                for intent_2 in classifier_2["classifier"]:
                                    if intent_2 in pregunta.lower():
                                        df.iloc[i, 5] = classifier_2["category"]
                                        break
                        else:
                            break
        return df

    def porcentaje_categoria(df, category):
        df_aux = df.query("categoria == @category")
        return (df_aux["id"].count() / df["id"].count())

    def porcentaje_especialidad(df, especialidad):
        df_aux = df.query("especialidad == @especialidad")
        return (df_aux["id"].count() / df["id"].count())

    def layout_factory(title, color='#D5D0CA',color_font="black"):
        layout = go.Layout(
            title=dict(text=title, y=0.92, x=0.5, xanchor='center', yanchor='top'),
            font=dict(color=color_font),
            hovermode='closest',
            margin=dict(r=0),
            titlefont={'color': "#151515", 'size': 20},
            paper_bgcolor=color,
            plot_bgcolor=color,
            legend=dict(orientation='v', bgcolor=color, xanchor='center', x=0.5, y=-0.5)
        )
        return layout

    def trace_patch_factory(color='#636EFA'):
        patch = dict(
            marker_color=color
        )
        return patch

    @app.callback(Output('interval-component', 'interval'), Input('interval_slider', 'value'))
    def update_chatbot(slider_value):
        return slider_value * 1000

    @app.callback(Output('pie_efic_chatbot', 'figure'), Output('histograma_uso_chatbot', 'figure'),
                  Output('mean_score_kpi', 'figure'), Output('line_chart_score', 'figure'),
                  Output('costo_kpi', 'figure'),Output('vacante_kpi', 'figure'),
                  Output('fecha_kpi', 'figure'),Output('tema_kpi', 'figure'),Output('puntaje_kpi', 'figure'),  Output('general_kpi', 'figure'),
                  Output('otros_kpi', 'figure'), Output('fig_pie_categorias_chatbot', 'figure'),
                  Output('fig_pie_especialidad_chatbot', 'figure'), Output('wordcloud_categorias', 'src'), Output('wordcloud_especialidades', 'src'),
                  Output('pie_dias_chatbot','figure'),Output('eficacia_kpi','figure'),Input('interval-component', 'n_intervals'))
    def update_chatbot(n):
        print(n)
        con = conexion(1)  # 1 para conexión con VPS/ 2 para conexión con Local

        data_preguntas_chatbot = pd.read_sql("SELECT * from pregunta", con)
        data_respuestas_chatbot = pd.read_sql("SELECT * from respuesta", con)
        con.close()

        # Pie
        eficienciaCB = data_preguntas_chatbot[['entendio', 'pregunta']]
        eficienciaCB = eficienciaCB.groupby(['entendio']).count()
        eficienciaCB['Descripcion'] = ['Errores', 'Éxitos']
        eficienciaCB = eficienciaCB.rename(columns={'pregunta': 'Cantidad'})
        fig_pie_efic_chatbot = px.pie(eficienciaCB, values='Cantidad', names='Descripcion')
        fig_pie_efic_chatbot.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie_efic_chatbot.update_layout(
            layout_factory(title="Eficacia del Chatbot"))
        fig_pie_efic_chatbot.update_layout(legend=dict(
            yanchor="top",
            y=0.0,
            xanchor="left",
            x=0.0
        ))

        # Histograma
        fig_fechas_histogram = px.histogram(data_preguntas_chatbot, x="fecha",
                                            title='Histograma del uso del chatbot', opacity=0.8)

        fig_fechas_histogram.update_layout(
            layout_factory(title=f"Histograma del uso del chatbot"))

        fig_fechas_histogram.update_layout(
            xaxis=dict(title='<b>Fecha y Hora</b>',
                       color='black',
                       showline=True,
                       showgrid=True),
            yaxis=dict(title='<b>Frecuencia</b>',
                       color='black',
                       showline=True,
                       showgrid=True),
        )

        fig_fechas_histogram.update_traces(patch=trace_patch_factory())

        # KPI: Mean score
        mean_score = data_respuestas_chatbot['score'].mean()
        mean_score_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=mean_score * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        mean_score_kpi.update_layout(
            layout_factory(title="Score de predicción promedio"))

        # Line chart score
        x_series = [i for i in range(0, len(list(data_respuestas_chatbot['answer'])))]
        fig_line_chart_score = px.line(data_respuestas_chatbot, x=x_series, y="score", title="Score de predicción")
        fig_line_chart_score.update_layout(
            layout_factory(title="Score de predicción"))
        fig_line_chart_score.update_layout(
            xaxis=dict(title='<b>Preguntas</b>',
                       color='black',
                       showline=True,
                       showgrid=True),
            yaxis=dict(title='<b>Score</b>',
                       color='black',
                       showline=True,
                       showgrid=True),
        )

        data_preguntas_chatbot = clasificador_pregunta(data_preguntas_chatbot)

        # KPI: Costo
        costo_porcentaje = porcentaje_categoria(data_preguntas_chatbot,"Costo")
        costo_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=costo_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        costo_kpi.update_layout(
            layout_factory(title="% de consultas sobre costos",color_font="black"))

        # KPI: Vacantes
        vacante_porcentaje = porcentaje_categoria(data_preguntas_chatbot,"Vacantes")
        vacante_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=vacante_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        vacante_kpi.update_layout(
            layout_factory(title="% de consultas por vacantes",color_font="black"))

        # KPI: Fecha
        fecha_porcentaje = porcentaje_categoria(data_preguntas_chatbot,"Fechas")
        fecha_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=fecha_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        fecha_kpi.update_layout(
            layout_factory(title="% de consultas sobre fechas",color_font="black"))

        # KPI: Tema
        tema_porcentaje = porcentaje_categoria(data_preguntas_chatbot,"Temas")
        tema_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=tema_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        tema_kpi.update_layout(
            layout_factory(title="% de consultas sobre temas",color_font="black"))

        # KPI: Puntaje
        puntaje_porcentaje = porcentaje_categoria(data_preguntas_chatbot, "Puntaje")
        puntaje_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=puntaje_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        puntaje_kpi.update_layout(
            layout_factory(title="% de consultas sobre el puntaje",color_font="black"))

        # KPI: General
        general_porcentaje = porcentaje_categoria(data_preguntas_chatbot, "Info general")
        general_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=general_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        general_kpi.update_layout(
            layout_factory(title="% de consultas generales",color_font="black"))

        # KPI: Otros
        otros_porcentaje = porcentaje_categoria(data_preguntas_chatbot, "Otros")
        otros_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=otros_porcentaje * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        otros_kpi.update_layout(
            layout_factory(title="% de consultas sobre otros temas", color_font="black"))

        consultas_categorizadas = data_preguntas_chatbot[['categoria', 'pregunta']]
        consultas_categorizadas = consultas_categorizadas.groupby(['categoria']).count()
        consultas_categorizadas.reset_index(level=0, inplace=True)
        consultas_categorizadas = consultas_categorizadas.rename(
            columns={'pregunta': 'Cantidad', 'categoria': "Categorias"})
        fig_pie_categorias_chatbot = px.pie(consultas_categorizadas, values='Cantidad', names='Categorias')
        fig_pie_categorias_chatbot.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie_categorias_chatbot.update_layout(
            layout_factory(title="Detalle de consultas al chatbot por categoría",color_font="black"))
        fig_pie_categorias_chatbot.update_layout(legend=dict(
            yanchor="top",
            y=0.0,
            xanchor="left",
            x=0.0
        ))

        consultas_especialidad= data_preguntas_chatbot[['especialidad', 'pregunta']]
        consultas_especialidad = consultas_especialidad.groupby(['especialidad']).count()
        consultas_especialidad.reset_index(level=0, inplace=True)
        consultas_especialidad = consultas_especialidad.rename(
            columns={'pregunta': 'Cantidad', 'especialidad': "Especialidades"})
        consultas_especialidad.drop([0], inplace=True)
        fig_pie_especialidad_chatbot = px.pie(consultas_especialidad, values='Cantidad', names='Especialidades')
        fig_pie_especialidad_chatbot.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie_especialidad_chatbot.update_layout(
            layout_factory(title="Detalle de consultas al chatbot por especialidad"))
        fig_pie_especialidad_chatbot.update_layout(legend=dict(
            yanchor="top",
            y=0.0,
            xanchor="left",
            x=0.0
        ))

        # WordCloud Categorias
        tendencia_categoria = data_preguntas_chatbot["categoria"]
        #plt.subplots(figsize=(10, 10))
        word_could_dict = Counter(list(tendencia_categoria))
        wordcloud = WordCloud(
            background_color='#D5D0CA',
            width=750,
            height=500
        ).generate_from_frequencies(word_could_dict)
        wordcloud = wordcloud.to_image()
        #plt.imshow(wordcloud, interpolation='bilinear')
        #plt.axis("off")
        img_categorias = BytesIO()
        wordcloud.save(img_categorias, format='PNG')
        src_categorias = 'data:image/png;base64,{}'.format(base64.b64encode(img_categorias.getvalue()).decode())


        # WordCloud Especialidades
        tendencia_especialidad = data_preguntas_chatbot["especialidad"]
        #plt.subplots(figsize=(10, 10))
        word_could_dict = Counter(list(tendencia_especialidad))
        wordcloud = WordCloud(
            background_color='#D5D0CA',
            width=750,
            height=500
        ).generate_from_frequencies(word_could_dict)
        wordcloud = wordcloud.to_image()
        #plt.imshow(wordcloud, interpolation='bilinear')
        #plt.axis("off")
        img_especialidad = BytesIO()
        wordcloud.save(img_especialidad, format='PNG')
        src_especialidad = 'data:image/png;base64,{}'.format(base64.b64encode(img_especialidad.getvalue()).decode())

        # pie_dias_chatbot
        cont_lunes = 0
        cont_martes = 0
        cont_miercoles = 0
        cont_jueves = 0
        cont_viernes = 0
        cont_sabado = 0
        cont_domingo = 0
        for index, row in data_preguntas_chatbot.iterrows():
            if row["fecha"].weekday() == 0:
                cont_lunes += 1
            if row["fecha"].weekday() == 1:
                cont_martes += 1
            if row["fecha"].weekday() == 2:
                cont_miercoles += 1
            if row["fecha"].weekday() == 3:
                cont_jueves += 1
            if row["fecha"].weekday() == 4:
                cont_viernes += 1
            if row["fecha"].weekday() == 5:
                cont_sabado += 1
            if row["fecha"].weekday() == 6:
                cont_domingo += 1

        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        count = [cont_lunes, cont_martes, cont_miercoles, cont_jueves, cont_viernes, cont_sabado, cont_domingo]
        d = {'Dias': dias, 'Cantidad': count}
        dff = pd.DataFrame(d)
        fig_pie_dias_chatbot = px.pie(dff, values='Cantidad', names='Dias', title='Porcentaje de Consulta por Días')
        fig_pie_dias_chatbot.update_layout(
            layout_factory(title="Porcentaje de consultas por días de la semana"))
        fig_pie_dias_chatbot.update_layout(legend=dict(
            yanchor="top",
            y=0.0,
            xanchor="left",
            x=0.0
        ))


        # KPI Eficacia

        eficacia = eficienciaCB.iloc[1, 0] / (eficienciaCB.iloc[0, 0] + eficienciaCB.iloc[1, 0])
        eficacia_kpi = go.Figure(data=go.Indicator(
            mode="number",
            # delta={'reference': max_likes},
            value=eficacia * 100,
            number=dict(
                suffix=' %',
                font={'size': 35}),
            domain={'y': [0, 1], 'x': [0, 1]},
        ),
            layout=go.Layout(
                title={
                    'text': 'Score en IMDb',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 25},
                    'pad': {'b': 20}
                },
                font=dict(color='black'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=150,
            )
        )
        eficacia_kpi.update_layout(
            layout_factory(title="Tasa de aciertos del chatbot"))


        return fig_pie_efic_chatbot, fig_fechas_histogram, mean_score_kpi, fig_line_chart_score, costo_kpi, vacante_kpi, \
               fecha_kpi, tema_kpi, puntaje_kpi, general_kpi, otros_kpi, fig_pie_categorias_chatbot, fig_pie_especialidad_chatbot, \
               src_categorias, src_especialidad, fig_pie_dias_chatbot, eficacia_kpi

    return
