"""fornecedores/urls.py - Rotas do app de fornecedores"""
from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    path('', views.lista_fornecedores, name='lista'),
    path('<int:pk>/', views.detalhe_fornecedor, name='detalhe'),
    path('novo/', views.criar_fornecedor, name='criar'),
    path('<int:pk>/editar/', views.editar_fornecedor, name='editar'),
    path('<int:pk>/excluir/', views.excluir_fornecedor, name='excluir'),
]
