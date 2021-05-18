from django.shortcuts import render
import pandas as pd
import numpy as np
import json


def index(request):
    # On precise en argument le séparateur des décimal ( pandas utilise "." )
    # On precise également un converter pour que le code département soit traité comme un string ( pour ne pas perdre les 0 pour les departement de 01 à 09 )
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|', decimal=',', converters={'Code departement': lambda x: str(x)})
    df.head()

    # On groupe par code departement et on fait la moyenne de la colonne par departement
    moyennevfpardep = df.groupby(['Code departement'])['Valeur fonciere'].mean().reset_index()

    # On renomme les colonnes pour convenir à highcharts
    moyennevfpardep.rename(columns={'Code departement': 'name'}, inplace=True)
    moyennevfpardep.rename(columns={'Valeur fonciere': 'y'}, inplace=True)

    # puis on format en json
    moyennevfpardep = moyennevfpardep.to_json(orient="records")

    # On prépare les variables que l'on va passer à la vue
    context = {'data': '', 'test':'','valeurfoncierepardep':moyennevfpardep }

    # On charge la vue avec les paramètres
    return render(request, 'graph/index.html', context)