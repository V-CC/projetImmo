from django.shortcuts import render
import pandas as pd
import numpy as np
import json


def index(request):
    df = pd.read_csv("valeursfoncieres-2020.txt",sep='|')
    df.head()
    prix = df[['Valeur fonciere','Code postal']].groupby('Code postal').count().sort_values(by='Valeur fonciere', ascending=False)
    prix.reset_index(0, inplace=True)
    prix.head()
    data= '[ 1 , 2 , 3 , 4]'
    context = {'data': data, 'prix':prix['Code postal'] }
    return render(request, 'graph/index.html', context)