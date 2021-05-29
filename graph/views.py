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

def index(request):
    return render(request, 'graph/index.html')

def france(request):
    df = pd.read_csv("valeursfoncieres-2020.txt", low_memory=False,sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    # Find the columns where each value is null
    cols_vides = [col for col in df.columns if df[col].isnull().all()]
    # Drop these columns from the dataframe
    df.drop(cols_vides,
        axis=1,
        inplace=True)
    df = df.fillna(0)

    moyennevfpardep = df.groupby(['Code departement'])['Valeur fonciere'].mean().reset_index()
    fig = px.bar(moyennevfpardep, x='Code departement', y='Valeur fonciere', height=600, width=700,
            title='Moyenne de la valeur foncière des ventes par département')
    
    graph = fig.to_html
    #graph.head(100)
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
    cols_vides = [col for col in df.columns if df[col].isnull().all()]
    # Drop these columns from the dataframe
    df.drop(cols_vides,
        axis=1,
        inplace=True)
    df = df.fillna(0)
    df = df.loc[df['Code departement'] == dep_id]
    df['Nombre de vente'] = df.groupby('Date mutation')['Commune'].transform('count')
    df['Date mutation'] = pd.to_datetime(df['Date mutation'])
    df.sort_values(by=['Date mutation'], inplace=True, ascending=False)
    df = df.loc[df['Type local'] == 'Maison']
    df['Prix metre carre'] = df.apply(lambda x: x['Valeur fonciere']/x['Surface reelle bati'] if x['Surface reelle bati'] > 0 else 0, axis=1)
    df = df[df['Prix metre carre'] >0]

    moyenneMetreCarreJour = df.groupby(['Date mutation'])['Prix metre carre'].mean().reset_index()

    figure1 = px.line(df, x="Date mutation", y="Nombre de vente", width=700)
    figure1.update_layout(title='Nombre de vente par jour ', xaxis_title="", yaxis_title="")
    figure2 = px.line(moyenneMetreCarreJour,title='Prix metre carre', x="Date mutation", y="Prix metre carre", width=700)
    figure1 = figure1.to_html
    figure2 = figure2.to_html
    context = {'codedep':dep_id,'figure1':figure1,'figure2':figure2}
    return render(request, 'graph/departement.html', context)

def commune(request,commune):
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|' , decimal=',', converters={'Code departement': lambda x: str(x)})
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
