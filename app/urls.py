from django.urls import path
from . import views

urlpatterns = [
    # Volúntarios
    path('voluntario', views.voluntario_lista),
    path('voluntario/<uuid:pk>', views.voluntario_detalhes),

    # Doações
    path('doacao', views.doacao_lista),
    path('doacao/<uuid:pk>', views.doacao_detalhes),

    # Região afetada
    path('regiao-afetada', views.regiao_lista),
    path('regiao-afetada/<uuid:pk>', views.regiao_detalhes),
]