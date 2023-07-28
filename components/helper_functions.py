 ######### Funções Auxiliares #########
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
from dash import dcc, html

###### Funções de Dados ######

# Extração de dados do banco de dados
def extract_data():
    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Obter a URI de conexão do banco de dados a partir das variáveis de ambiente
    db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Criar a engine de conexão
    engine = create_engine(db_uri)

    # Consultar a tabela 'alldata' e carregar os dados em um DataFrame
    query = "SELECT * FROM alldata"
    df = pd.read_sql_query(query, engine)

    return df

# 1º tratamento
def transform_data(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['status'] = df['status'].astype(str)
    df['assignee'] = df['assignee'].astype(str)
    return df

def df_ind(df):
    
    # Determina o numero de dias que a card_id possui desde a data inicial do projeto
    df['age'] = round((pd.to_datetime('today') - df['created_at']).dt.days, 2)
    
    # Calcula o tempo de conclusão e preenche os valores NaN com zero
    df['time_to_complete'] = round((df['closed_at'] - df['created_at']).dt.days, 2)

    # Preenche os valores NaN na coluna 'tempo_conclusao' com zero
    df['time_to_complete'].fillna(0, inplace=True)

    # Na coluna 'numero_manutencoes' é adicionado o número de vezes que o card_id entrou em manutenção, como não temos essa informação, coloque um número aleatório entre 0 e 10
    df['maintenance_count'] = np.random.randint(0, 11, size=len(df))
    
    # Preenche a coluna 'maintenance_rate' com dados aleatórios entre 0% e 100%
    df['maintenance_rate_%'] = np.random.uniform(0, 100, size=len(df))
    df['maintenance_rate_%'] = round(df['maintenance_rate_%'], 2)

    # Preenche a coluna 'bug_rate' com dados aleatórios entre 0% e 100%
    df['bug_rate_%'] = np.random.uniform(0, 100, size=len(df))
    df['bug_rate_%'] = round(df['bug_rate_%'], 2)

    # Preenche a coluna 'block_rate' com dados aleatórios entre 0% e 100%
    df['block_rate_%'] = np.random.uniform(0, 100, size=len(df))
    df['block_rate_%'] = round(df['block_rate_%'], 2)
    
    return df

def df_ind_pessoal(df):
    # Cria um novo dataframe com as colunas desejadas
    df_ind_pessoal = pd.DataFrame(columns=['assignee', 'numero_tarefas', 'tempo_trabalho'])

    return df_ind_pessoal

###### Funções de Plot ######

# Cards

def create_card(title, value, trend):
    
    card_header = dbc.CardHeader(title, className="class_card_header")
    card_body = dbc.CardBody(
        [
            html.H3(value, className="class_card_title"),
            html.P(trend, className="class_card_text"),
        ]
    )
    card = dbc.Card([card_header, card_body], className="class_card")

    return card

# Indicadores

def productivity(df):
    # Indica a produtividade, ou seja, o número total de tarefas concluídas em um determinado período de tempo.
    return df['numero_tarefas'].sum()

def quality(df):
    # Indica a qualidade, medindo o total de bugs encontrados em tarefas concluídas.
    return df['bug_rate_%'].sum()

def wip(df):
    # Indica o trabalho em andamento (Work in Progress), contando o número de tarefas que estão atualmente em andamento.
    return df['status'].value_counts()['open']

def stale_work(df):
    # Indica o trabalho pendente, contando o número de tarefas que estão atualmente pendentes.
    if 'pending' in df['status'].values:
        return df['status'].value_counts()['pending']
    else:
        return 0

def current_blocked_items(df):
    # Indica o número atual de tarefas bloqueadas, ou seja, tarefas que não podem progredir devido a algum impedimento.
    if 'blocked' in df['status'].values:
        return df['status'].value_counts()['blocked']
    else:
        return 0

def days_lost_to_blocked(df):
    # Indica o número total de dias perdidos devido a tarefas bloqueadas.
    return df.loc[df['status'] == 'blocked', 'time_to_complete'].sum()
    
# Gráficos

def plot_histogram_status(df):
    status_counts = df['status'].value_counts()

    fig = go.Figure(data=[go.Bar(x=status_counts.index, y=status_counts.values)])
    fig.update_layout(
        title='Histogram of Status',
        xaxis_title='Status',
        yaxis_title='Count'
    )
    return fig

def plot_histogram_blocked_vs_unblocked(df):
    blocked = df[df['status'] == 'blocked'].shape[0]
    unblocked = df[df['status'] != 'blocked'].shape[0]

    fig = go.Figure(data=[go.Bar(x=['Blocked', 'Unblocked'], y=[blocked, unblocked])])
    fig.update_layout(
        title='Histogram of Blocked Vs. Unblocked',
        xaxis_title='Status',
        yaxis_title='Count'
    )
    return fig

def plot_line_chart_by_month(df, indicator):
    df['month'] = pd.to_datetime(df['closed_at']).dt.month
    indicator_sum_by_month = df.groupby('month')[indicator].sum()

    fig = go.Figure(data=[go.Scatter(x=indicator_sum_by_month.index, y=indicator_sum_by_month.values, mode='markers+lines')])
    fig.update_layout(
        title=f'Line Chart of {indicator} by Month',
        xaxis_title='Month',
        yaxis_title=indicator
    )
    return fig
