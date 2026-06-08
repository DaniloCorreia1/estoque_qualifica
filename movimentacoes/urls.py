"""movimentacoes/urls.py"""
from django.urls import path
from . import views

app_name = 'movimentacoes'

urlpatterns = [
    path('', views.lista_movimentacoes, name='lista'),
    path('entrada/', views.registrar_entrada, name='entrada'),
    path('saida/', views.registrar_saida, name='saida'),
    path('ajuste/', views.registrar_ajuste, name='ajuste'),
    path('<int:pk>/', views.detalhe_movimentacao, name='detalhe'),
]
