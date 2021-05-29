from django.shortcuts import render
import pandas as pd
import numpy as np
import json
# datetime oprations
from datetime import timedelta
# to get web contents
from urllib.request import urlopen
# basic visualization package
import matplotlib.pyplot as plt

# interactive visualization
import plotly.express as px
import plotly.graph_objs as go
# import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# basic visualization package
import matplotlib.pyplot as plt


# interactive visualization
import plotly.express as px
import plotly.graph_objs as go
# import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from common.utils.graphtohtml import DataToGraphUtils


def index(request):
    return render(request, 'graph/index.html')

def france(request):
    df = pd.read_csv("valeursfoncieres-2020.txt", low_memory=False,sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df.head()
    moyennevfpardep = df.groupby(['Code departement'])['Valeur fonciere'].mean().reset_index()
    fig = px.bar(moyennevfpardep, x='Code departement', y='Valeur fonciere', height=600, width=700,
             title='Moyenne de la valeur foncière des ventes par département')
    graph = fig.to_html

    moyennesurface =  df.groupby(['Code departement'])['Surface reelle bati'].mean().reset_index()
    fig2 = px.bar(moyennesurface, x='Code departement', y='Surface reelle bati', height=600, width=700,
                 title='Moyenne de la Surface reelle bati des ventes par département')
    graph2 = fig2.to_html();
    # On prépare les variables que l'on va passer à la vue
    context = {'figure1': graph,'figure2':graph2 }
    return render(request, 'graph/france.html', context)

def searchdep(request):
    return render(request, 'graph/searchdep.html')

def searchcommune(request):
    return render(request, 'graph/searchcommune.html')


def departement(request,dep_id):
    dep_id = str(dep_id)
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df.head()
    df = df.loc[df['Code departement'] == dep_id]
    vente = df
    vente['Nombre de vente'] = vente.groupby('Date mutation')['Commune'].transform('count')
    vente['Date mutation'] = pd.to_datetime(vente['Date mutation'])
    vente.sort_values(by=['Date mutation'], inplace=True, ascending=False)
    vente.head()
    figure1 = DataToGraphUtils.plot_daywise(vente,'Nombre de vente')
    context = {'codedep':dep_id,'figure1':figure1}
    return render(request, 'graph/departement.html', context)

def commune(request,commune):
    commune = commune.replace('_',' ')
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df = df.loc[df['Commune'] == commune]
    df.head()
    vente = df
    vente['Nombre de vente'] = vente.groupby('Date mutation')['Commune'].transform('count')
    vente['Date mutation'] = pd.to_datetime(vente['Date mutation'])
    vente.sort_values(by=['Date mutation'], inplace=True, ascending=False)
    vente.head()
    figure1 = DataToGraphUtils.plot_daywise(vente,'Nombre de vente')
    df['vente'] = 1
    filtered_df = df[df['Type local'].notnull()]
    figure2 = px.pie(filtered_df, values='vente', names='Type local', title='repartition nombre de ventes')
    figure2 = figure2.to_html()
    figure3 = px.pie(filtered_df, values='Valeur fonciere', names='Type local', title='repartition valeurs foncière')
    figure3 = figure3.to_html()
    context = {'commune':commune,'figure1':figure1,'figure2':figure2,'figure3':figure3}
    return render(request, 'graph/commune.html', context)

def about(request):
    return render(request, 'graph/about.html')
