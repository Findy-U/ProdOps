import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from components import helper_functions as hf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Dados de exemplo
#df = pd.read_csv('ProdOps\database\Data.csv')
df = hf.extract_data()
print(df.head())

######### Estilos das Classes #########

# Layout
class_layout1 = "header"

# Cabeçalho
class_h1 = "text-center h1"
class_h2 = "text-center h2"
class_h3 = "text-center h3"

# Conteúdo
class_p1 = "text-p"
class_l1 = "my-legend"
# Label
class_label1= "label1"
class_label2= "label2"

# Botão
class_button = "button"

# Card
class_card = "card"
class_card2 = "card2"
class_card_header = "card-header"
class_card_title = "card-title"
class_card_text = "card-title"

# Divs e Cols
class_div = "div_highlight"
class_row = "row_highlight"
class_col = "col_highlight"

# Graph
class_graph = "graph-container"

# Dropdown
class_dropdown = "dropdown"

# Date pick
class_datepickerrange = "form-control"

# Checklist
class_checklist = "form-check-input"


######### Tratamento de Dados #########

DF_main = hf.transform_data(df)

DF_ind = DF_main.copy()

DF_ind = hf.df_ind(DF_ind)

# Criação de Indicadores

DF_ind_pessoal = hf.df_ind_pessoal(DF_ind)

######### Layout do Dashboard #########

layout = dbc.Container(
    fluid=True,
    children=[
        
        
        ######### Dashboard #########
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    [
                        ######### Sidebar #########
                        dbc.Col(
                            [
                                dbc.Button(
                                    "Atualizar",
                                    id="Atualizar",
                                    className=class_button,
                                ),
                                
                                ######### Filtro dropdown #########
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H3("Categorias", 
                                                    className=class_h3, 
                                                    )
                                        ),    
                                        dbc.CardBody(
                                            [
                                                html.Label("Categoria 1",
                                                           className=class_label1, 
                                                           ),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dropdown-cat1",
                                                        clearable=False,
                                                        className=class_dropdown,                                                        
                                                        persistence=True,
                                                        persistence_type="session",
                                                        multi=True,
                                                    )
                                                ),
                                                html.Label("Categoria 2", 
                                                           className=class_label1),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dropdown-cat2",
                                                        clearable=False,
                                                        className=class_dropdown,
                                                        persistence=True,
                                                        persistence_type="session",
                                                        multi=True,
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    className=class_card,
                                ),
                                
                                ######### Filtro checklist #########
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H3("Opções", 
                                                    className=class_h3, 
                                                    )
                                        ),
                                        dbc.CardBody(
                                            dbc.Checklist(
                                                options=[
                                                    {"label": "Opção 1", "value": "opcao1"},
                                                    {"label": "Opção 2", "value": "opcao2"},
                                                    {"label": "Opção 3", "value": "opcao3"}
                                                ],
                                                value=["opcao1"],
                                                className=class_checklist,
                                                
                                            )
                                        )
                                    ],
                                    className=class_card,
                                    
                                ),

                                ######### Filtro Período #########
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H3("Período", 
                                                    className=class_h3, 
                                                    )
                                        ),
                                        dbc.CardBody(
                                            dcc.DatePickerRange(
                                                start_date="2023-01-01",
                                                end_date="2023-12-31",
                                                className=class_datepickerrange,
                                                
                                            )
                                        )
                                    ],
                                    className=class_card,
                                    
                                )
                            ],
                            className=class_col,
                            width=2
                        ),

                        ######### Indicadores #########
                        dbc.Col(
                            [
                                ######### Cabeçalho #########
                                dbc.Row(
                                    [
                                    dbc.Col(
                                        html.H1(
                                            "Desempenho",
                                            className=class_h1,
                                        ),
                                        width=10
                                    ),
                                    dbc.Col(
                                        html.P(f"Última atualização: {pd.to_datetime('today').strftime('%Y-%m-%d')}",
                                            className=class_p1,
                                            ),
                                            width=2
                                    )
                                    ]
                                
                                ),
                
                                ######### Valores únicos #########
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            hf.create_card("Productivity", hf.productivity(DF_ind_pessoal), ""),
                                            width=3
                                        ),
                                        dbc.Col(
                                            hf.create_card("Batata", hf.productivity(DF_ind_pessoal), ""),
                                            width=3
                                        ),
                                        dbc.Col(
                                            hf.create_card("WIP (Work in Progress)", hf.wip(DF_ind), ""),
                                            width=3
                                        ),
                                        dbc.Col(
                                            hf.create_card("Stale Work", hf.stale_work(DF_ind), "↑"),
                                            width=3
                                        ),
                                    ],
                                    className=class_row,
                                    justify="center",
                                    align="center",
                                ),
                                
                                ######### Gráficos Superiores #########
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Graph(figure=hf.plot_histogram_status(DF_main),
                                                className=class_graph,
                                                         )
                                            ],
                                            width=6
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Graph(figure=hf.plot_histogram_status(DF_main),
                                                className=class_graph,
                                                        )
                                            ],
                                            width=6,
                                        )
                                    ]
                                ),
                                
                                ######### Gráficos Inferiores #########
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Graph(figure=hf.plot_histogram_blocked_vs_unblocked(DF_main),
                                                className=class_graph,
                                                        )
                                            ],
                                            width=6
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Graph(figure=hf.plot_histogram_blocked_vs_unblocked(DF_main),
                                                className=class_graph,
                                                        )
                                            ],
                                            width=6
                                        )
                                    ]
                                )
                            
                            ],
                            className=class_col,
                            width=10
                        )
                    ],
                    className=class_row
                )
            ],
            className=class_layout1,
        ),
    ],
    style={'font-family': 'Arial'}
)