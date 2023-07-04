from dash import html

def create_sidebar():
    return html.Div(
        children=[
            html.H3('Menu Lateral'),
            html.Button('Opção 1', id='button-1'),
            html.Button('Opção 2', id='button-2'),
            html.Button('Opção 3', id='button-3'),
            # Adicione mais botões ou componentes do menu lateral conforme necessário
        ],
        className='sidebar',
        style={'width': '15%', 'padding': '20px', 'background-color': 'lightgray', 'height': '100vh'}
    )
