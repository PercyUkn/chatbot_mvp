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
        #external_scripts=['/static/js_dashboard/99_custom-js.js']
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
                dbc.NavLink("Cerrar sesión", href="/logout", class_name="logout",id="logout_button"),
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

                    # Chatbot
                    html.Div([
                        # Pie del chatbot
                        html.Div([
                            dcc.Graph(  # figure=fig_duration_box,
                                className="dcc-compon",
                                config={'displayModeBar': 'hover'},
                                id="pie_efic_chatbot")
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

                    # Nube de palabras
                    html.Div([
                        # Nube de palabras
                        html.Div([

                            html.H5("Palabras más usadas", style={"marginBottom": '0px', 'color': 'black'}),
                            html.Img(title="Nube de palabras", id="wordcloud_CB"),

                        ], className="card_container twelve columns", style={'textAlign': 'center'}),
                        # Boton refresh
                        #  html.Div([
                        #      html.A(html.Button('Actualizar', id="refresh"), href='/'),
                        #  ], className="card_container two columns", style={'textAlign': 'center'}),
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

    def layout_factory(title, color='#D5D0CA'):
        layout = go.Layout(
            title=dict(text=title, y=0.92, x=0.5, xanchor='center', yanchor='top'),
            font=dict(color='white'),
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
                  Input('interval-component', 'n_intervals'))
    def update_chatbot(n):
        print(n)
        con = conexion(1) # 1 para conexión con VPS/ 2 para conexión con Local

        data_chatbot = pd.read_sql("SELECT * from pregunta", con)

        # Pie
        eficienciaCB = data_chatbot[['entendio', 'pregunta']]
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
        fig_fechas_histogram = px.histogram(data_chatbot, x="fecha",
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
        con.close()
        return fig_pie_efic_chatbot, fig_fechas_histogram

    return
