import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import calendar
import plotly.graph_objects as go

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin = dict(l=25, r=25, t=25, b=0)

# Carregar os dados do arquivo CSV
df = pd.read_csv('database/Data.csv')

# Criar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


######### Estilos das Classes #########

# Layout
class_layout = "mx-0"
style_layout = {}
class_layout2 = "container-fluid"
style_layout2 = {"padding": "0"}

# Botão
class_button = "btn btn-primary"
style_button = {"margin-bottom": "10px"}
class_button2 = "btn btn-secondary"
style_button2 = {"margin-top": "10px"}

# Card
class_card = "card"
style_card = {"padding": "20px"}
class_card2 = "card text-white bg-primary"
style_card2 = {"padding": "15px", "border-radius": "5px"}

# Divs
class_div1 = "class_div_highlight"
style_div1 = {"maxWidth": 75, "height": 100, "marginLeft": "-10px"}

# Graph
class_graph = "graph-container"
style_graph = {"height": "300px"}
class_graph2 = "graph-container-large"
style_graph2 = {"height": "500px"}

# Dropdown
class_dropdown = "dropdown"
style_dropdown = {"width": "200px"}
class_dropdown2 = "dropdown-menu"
style_dropdown2 = {"width": "300px"}


######### Layout do Dashboard #########

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Button(
                            "Aplicar Filtros",
                            id="btn-aplicar-filtros",
                            className=class_button,
                            style=style_button
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.Legend(
                                                    "Filtrar lançamentos",
                                                    className=class_card,
                                                ),
                                                html.Label(
                                                    "Categorias das receitas"
                                                ),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dropdown-receita",
                                                        clearable=False,
                                                        style=style_dropdown,
                                                        persistence=True,
                                                        persistence_type="session",
                                                        multi=True,
                                                    )
                                                ),
                                                html.Label(
                                                    "Categorias das despesas",
                                                    style=style_card,
                                                ),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dropdown-despesa",
                                                        clearable=False,
                                                        style=style_dropdown,
                                                        persistence=True,
                                                        persistence_type="session",
                                                        multi=True,
                                                    )
                                                ),
                                                html.Label(
                                                    "Tags",
                                                    style={"marginTop": "10px"},
                                                ),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dropdown-tag",
                                                        clearable=False,
                                                        style=style_dropdown,
                                                        persistence=True,
                                                        persistence_type="session",
                                                        multi=True,
                                                    )
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            className=class_card,
                                            style=style_card,
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.Legend(
                                                    "Filtrar lançamentos",
                                                    className=class_card,
                                                ),
                                                html.Label("Período"),
                                                html.Div(
                                                    dcc.DatePickerRange(
                                                        id="date-picker-range",
                                                        style=style_dropdown,
                                                        persistence=True,
                                                        persistence_type="session",
                                                    )
                                                ),
                                                html.Label(
                                                    "Filtros",
                                                    style=style_card,
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Checklist(
                                                            options=[
                                                                {
                                                                    "label": "Receitas",
                                                                    "value": "receita",
                                                                },
                                                                {
                                                                    "label": "Despesas",
                                                                    "value": "despesa",
                                                                },
                                                                {
                                                                    "label": "Transfers",
                                                                    "value": "transfer",
                                                                },
                                                            ],
                                                            value=[
                                                                "receita",
                                                                "despesa",
                                                                "transfer",
                                                            ],
                                                            id="checklist-tipos",
                                                            inline=True,
                                                            className=class_card,
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Checklist(
                                                            options=[
                                                                {
                                                                    "label": "Lançamentos futuros",
                                                                    "value": "futuro",
                                                                }
                                                            ],
                                                            value=[],
                                                            id="checklist-status",
                                                            inline=True,
                                                            className=class_card,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            className=class_card,
                                            style=style_card,
                                        )
                                    ],
                                    width=6,
                                ),
                            ],
                            className=class_layout,
                        ),
                    ],
                    width=2,
                    className="bg-dark p-3 text-dark text-center",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.CardGroup(
                                            [
                                                dbc.Card(
                                                    [
                                                        html.Legend("Saldo"),
                                                        html.H5(
                                                            "R$ -",
                                                            id="p-saldo-dashboards",
                                                            style={},
                                                        ),
                                                    ],
                                                    className=class_card,
                                                    style=style_card,
                                                ),
                                                dbc.Card(
                                                    [
                                                        html.Legend("Receitas"),
                                                        html.H5(
                                                            "R$ -",
                                                            id="p-receita-dashboards",
                                                            style={},
                                                        ),
                                                    ],
                                                    className=class_card,
                                                    style=style_card,
                                                ),
                                                dbc.Card(
                                                    [
                                                        html.Legend("Despesas"),
                                                        html.H5(
                                                            "R$ -",
                                                            id="p-despesa-dashboards",
                                                            style={},
                                                        ),
                                                    ],
                                                    className=class_card,
                                                    style=style_card,
                                                ),
                                            ],
                                            className=class_card,
                                        ),
                                    ],
                                    width=6,
                                    className="mb-4",
                                ),
                            ],
                            className=class_layout,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.Legend(
                                                    "Resumo das Categorias",
                                                    className="card-title",
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="graph-categorias",
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                            style=style_graph,
                                                        )
                                                    ],
                                                    className="p-2",
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            className=class_card,
                                            style=style_card,
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                html.Legend(
                                                    "Resumo das Categorias",
                                                    className="card-title",
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="graph-categorias2",
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                            style=style_graph,
                                                        )
                                                    ],
                                                    className="p-2",
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            className=class_card,
                                            style=style_card,
                                        )
                                    ],
                                    width=6,
                                ),
                            ],
                            className=class_layout,
                            style=style_layout,
                        ),
                    ],
                    width=10,
                    className="bg-primary text-black p-3 text-center",
                ),
            ],
            className=class_layout,
            style=style_layout,
        ),
    ],
    fluid=True,
    className=class_layout2,
    style=style_layout2,
)



# Iniciar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
