import os
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from components.layouts import dashboard_layout
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Obtém o caminho completo para o arquivo styles.css
css_path = os.path.join(os.path.dirname(__file__), 'assets/css/styles.css')

# Criação do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, css_path])

# Layout do dashboard
app.layout = dashboard_layout.layout

if __name__ == '__main__':
    app.run_server(debug=True)
