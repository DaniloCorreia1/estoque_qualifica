"""produtos/urls.py"""
from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista_produtos, name='lista'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe'),
    path('novo/', views.criar_produto, name='criar'),
    path('<int:pk>/editar/', views.editar_produto, name='editar'),
    path('<int:pk>/excluir/', views.excluir_produto, name='excluir'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
]
