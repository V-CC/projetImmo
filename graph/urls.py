from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchdep', views.searchdep, name='searchdep'),
    path('searchcommune', views.searchcommune, name='searchcommune'),
    path('france', views.france, name='france'),
    path('departement/<int:dep_id>', views.departement, name='departement'),
    path('commune/<slug:commune>', views.commune, name='commune'),
    path('about', views.about, name='about'),
]