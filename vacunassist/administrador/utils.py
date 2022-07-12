import enum
from turtle import width
import numpy as np
import pandas as pd
import uuid, base64
from .models import *
from io import BytesIO
from matplotlib import pyplot


def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]

def get_key(res_by):
    if res_by == '#1':
        key = 'solicitud_id'
    elif res_by == '#2':
        key = 'solicitud_id'
    elif res_by == '#3':
        key = 'solicitud_id'
    elif res_by == '#4':
        key = 'solicitud_id'
    return key

def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart_solicitud(data, centro, **kwargs):
    pyplot.switch_backend('AGG')
    pyplot.figure(figsize=(10, 4))
    # fig = pyplot.figure(figsize=(12, 4))
    # key = get_key(results_by)

    nombres_vacuna = {
        1 : 'Covid (1ra)',
        2 : 'Covid (2da)',
        3 : 'Gripe',
        4 : 'Fiebre Amarilla',
    }
    line_color = {
        1 : 'red',
        2 : 'green',
        3 : 'blue',
        4 : 'yellow',
    }

    d = data.sort_values('fecha_estimada', ascending=True).query(f"centro_vacunatorio=='{centro}'").groupby(['fecha_estimada', 'vacuna_id'], as_index=False)['solicitud_id'].agg('count')

    try:
        vacunas = list(d['vacuna_id'].unique())
        for vacuna in [1, 2, 3, 4]:
            # si no hay solicitudes para algún centro, se agrega un valor para que aparezca la línea
            if vacuna not in vacunas:
                d = d.append({
                    'vacuna_id' : vacuna,
                    'solicitud_id' : 0,
                    'fecha_estimada' : d.iat[0,0],
                    }, ignore_index=True)
    except Exception:
        return False

    d = pd.pivot_table(d, index=['fecha_estimada', 'vacuna_id'], values='solicitud_id', fill_value=0, dropna=False, aggfunc=np.sum).reset_index()
    d['fecha_estimada'] = d['fecha_estimada'].apply(lambda x: x.strftime('%d/%m/%Y'))

    xlabels = d['fecha_estimada'].unique()
    for vacuna in [1, 2, 3, 4]:
        fechas = d.query(f"vacuna_id=='{vacuna}'")['fecha_estimada']
        cantidades = d.query(f"vacuna_id=='{vacuna}'")['solicitud_id']

        pyplot.plot(xlabels, d.query(f"vacuna_id=={vacuna}")['solicitud_id'], color=line_color[vacuna], marker='o', linestyle='-.', linewidth=1, label=nombres_vacuna[vacuna])

    pyplot.title(f'Centro: {centro}')
    pyplot.xlabel('Fecha de Solicitud')
    pyplot.ylabel('Solicitudes Recibidas')
    pyplot.tight_layout()
    pyplot.legend()
    chart = get_graph()
    
    return chart


def get_chart_turnos(data, centro, **kwargs):
    pyplot.switch_backend('AGG')
    pyplot.figure(figsize=(10, 4))
    # fig = pyplot.figure(figsize=(12, 4))
    # key = get_key(results_by)

    nombres_vacuna = {
        1 : 'Covid (1ra)',
        2 : 'Covid (2da)',
        3 : 'Gripe',
        4 : 'Fiebre Amarilla',
    }
    line_color = {
        1 : 'red',
        2 : 'green',
        3 : 'blue',
        4 : 'yellow',
    }

    d = data.sort_values('fecha_confirmada', ascending=True).query(f"centro_vacunatorio=='{centro}'").groupby(['fecha_confirmada', 'vacuna_id'], as_index=False)['turno_id'].agg('count')

    try:
        vacunas = list(d['vacuna_id'].unique())
        for vacuna in [1, 2, 3, 4]:
            # si no hay solicitudes para algún centro, se agrega un valor para que aparezca la línea
            if vacuna not in vacunas:
                d = d.append({
                    'vacuna_id' : vacuna,
                    'turno_id' : 0,
                    'fecha_confirmada' : d.iat[0,0],
                    }, ignore_index=True)
    except Exception:
        return False

    d = pd.pivot_table(d, index=['fecha_confirmada', 'vacuna_id'], values='turno_id', fill_value=0, dropna=False, aggfunc=np.sum).reset_index()
    d['fecha_confirmada'] = d['fecha_confirmada'].apply(lambda x: x.strftime('%d/%m/%Y'))

    xlabels = d['fecha_confirmada'].unique()
    for vacuna in [1, 2, 3, 4]:
        fechas = d.query(f"vacuna_id=='{vacuna}'")['fecha_confirmada']
        cantidades = d.query(f"vacuna_id=='{vacuna}'")['turno_id']

        pyplot.plot(xlabels, d.query(f"vacuna_id=={vacuna}")['turno_id'], color=line_color[vacuna], marker='o', linestyle='-.', linewidth=1, label=nombres_vacuna[vacuna])

    pyplot.title(f'Centro: {centro}')
    pyplot.xlabel('Fecha de Turno')
    pyplot.ylabel('Turnos Esperados')
    pyplot.tight_layout()
    pyplot.legend()
    chart = get_graph()
    
    return chart