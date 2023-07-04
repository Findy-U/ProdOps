 ######### Funções Auxiliares #########
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime


def plot_status_histogram(df):
    # Criar histograma de contagem de valores na coluna 'status'
    counts = df['status'].value_counts()

    # Criar figura do histograma
    fig = go.Figure(data=[go.Bar(x=counts.index, y=counts.values)])

    # Configurar layout da figura
    fig.update_layout(
        title='Quantidades Status',
        xaxis_title='Status',
        yaxis_title='Contagem'
    )
    
    return fig

# 1º tratamento
def transform_data(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['status'] = df['status'].astype(str)
    df['assignee'] = df['assignee'].astype(str)
    return df


def df_ind_pessoal(df):
    # Cria um novo dataframe com as colunas desejadas
    df_ind_pessoal = pd.DataFrame(columns=['assignee', 'numero_tarefas', 'tempo_trabalho'])

    # Agrupa os dados por assignee e realiza as operações de contagem e soma
    df_grouped = df.groupby('assignee').agg({'project_card_id': 'count', 'closed_at': 'sum'})

    # Preenche o novo dataframe com os valores calculados
    df_ind_pessoal['assignee'] = df_grouped.index
    df_ind_pessoal['numero_tarefas'] = df_grouped['project_card_id']
    df_ind_pessoal['tempo_trabalho'] = df_grouped['closed_at']

    return df_ind_pessoal


def df_ind_tarefas(df):
    # Cria um novo dataframe com as colunas desejadas
    df_ind_tarefas = pd.DataFrame(columns=['project_card_id', 'tempo_conclusao', 'numero_manutencoes'])

    # Na coluna project_card_id cria uma linha para cada valor único da coluna project_card_id e os aloca em ordem crescente.
    df_ind_tarefas['project_card_id'] = df['project_card_id'].unique()
    df_ind_tarefas = df_ind_tarefas.sort_values('project_card_id')

    # Calcula o tempo de conclusão e preenche os valores NaN com zero
    for card_id in df_ind_tarefas['project_card_id']:
        data_hora1 = df[df['project_card_id'] == card_id]['created_at']
        data_hora2 = df[df['project_card_id'] == card_id]['closed_at']

        diferenca = data_hora2 - data_hora1
        diferenca_em_dias = diferenca.dt.days
        diferenca_em_dias_arredondada = round(diferenca_em_dias, 2)

        df_ind_tarefas.loc[df_ind_tarefas['project_card_id'] == card_id, 'tempo_conclusao'] = diferenca_em_dias_arredondada

    # Preenche os valores NaN na coluna 'tempo_conclusao' com zero
    df_ind_tarefas['tempo_conclusao'].fillna(0, inplace=True)

    # Na coluna 'numero_manutencoes' é adicionado o número de vezes que o card_id entrou em manutenção, como não temos essa informação, coloque um número aleatório entre 0 e 10
    df_ind_tarefas['numero_manutencoes'] = np.random.randint(0, 11, size=len(df_ind_tarefas))

    return df_ind_tarefas
