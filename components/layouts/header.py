from dash import html
import pandas as pd

def create_header():
    return html.Div(
        children=[
            html.H1(
                "Dashboard de Projetos do GitHub",
                style={
                    'textAlign': 'center',
                    'color': 'gray',
                    'backgroundColor': 'navy',
                    'padding': '2%',
                    'margin': '2%',
                    'border': '5px solid black',
                    'fontSize': '24px',
                    'fontWeight': 'bolder',
                    'fontStyle': 'normal',
                    'textDecoration': 'normal',
                    'textTransform': 'capitalize',
                    'letterSpacing': '2%',
                    'lineHeight': '3',
                    'width': '90%',
                    'height': '10%',
                    'fontFamily': 'Arial, sans-serif',
                    'textShadow': '4px 4px 8px #000000',
                    'boxShadow': '0px 0px 5px rgba(0, 0, 0, 0.3)',
                    'borderRadius': '2%',
                    'opacity': '0.9',
                    'cursor': 'pointer',
                }
            ),
            html.P(f"Última atualização: {pd.to_datetime('today').strftime('%Y-%m-%d')}",
                   style={'textAlign': 'center'})
        ],
        className="header",
        style={'backgroundColor': 'lightgray', 'padding': '20px'}
    )
