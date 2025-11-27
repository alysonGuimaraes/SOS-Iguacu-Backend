from django.urls import path
from . import views

urlpatterns = [
    # Volúntarios
    path('voluntario', views.voluntario_lista, name='voluntario_lista'),
    path('voluntario/<uuid:pk>', views.voluntario_detalhes, name='voluntario_detalhes'),

    # Doações
    path('doacao', views.doacao_lista, name='doacao_lista'),
    path('doacao/<uuid:pk>', views.doacao_detalhes, name='doacao_detalhes'),

    # Região afetada
    path('regiao-afetada', views.regiao_lista, name='regiao_lista'),
    path('regiao-afetada/<uuid:pk>', views.regiao_detalhes, name='regiao_detalhes'),

    # APIs externas
    path('consulta-cep/<str:cep>', views.busca_cep, name='busca-cep'),
]