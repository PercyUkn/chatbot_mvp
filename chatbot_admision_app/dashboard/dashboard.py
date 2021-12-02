import dash
from dash import html, callback
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


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/css_dashboard/custom-style.css',
            '/static/css_dashboard/s1-plotly.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container')

    return dash_app.server