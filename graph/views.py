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



def index(request):
    return render(request, 'graph/index.html')

def france(request):
    df = pd.read_csv("valeursfoncieres-2020.txt", low_memory=False,sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df.head()
    moyennevfpardep = df.groupby(['Code departement'])['Valeur fonciere'].mean().reset_index()
    fig = px.bar(moyennevfpardep, x='Code departement', y='Valeur fonciere', height=600, width=700,
             title='Moyenne de la valeur foncière des ventes par département')
    graph = fig.to_html
    # On prépare les variables que l'on va passer à la vue
    context = {'figure1': graph }
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
    figure1 = px.line(vente, x="Date mutation", y="Nombre de vente", width=700)
    figure1.update_layout(title='Nombre de vente par jour ', xaxis_title="", yaxis_title="")
    figure1 = figure1.to_html
    context = {'codedep':dep_id,'figure1':figure1}
    return render(request, 'graph/departement.html', context)

def commune(request,commune):
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df.head()
    df = df.loc[df['Commune'] == commune]
    vente = df
    vente['Nombre de vente'] = vente.groupby('Date mutation')['Commune'].transform('count')
    vente['Date mutation'] = pd.to_datetime(vente['Date mutation'])
    vente.sort_values(by=['Date mutation'], inplace=True, ascending=False)
    vente.head()
    figure1 = px.line(vente, x="Date mutation", y="Nombre de vente", width=700)
    figure1.update_layout(title='Nombre de vente par jour ', xaxis_title="", yaxis_title="")
    figure1 = figure1.to_html
    context = {'commune':commune,'figure1':figure1}
    return render(request, 'graph/commune.html', context)

def about(request):
    return render(request, 'graph/about.html')
