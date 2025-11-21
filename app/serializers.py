from rest_framework import serializers
from .models import Voluntario, RegiaoAfetada, Doacao

class VoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntario
        fields = '__all__'

class RegiaoAfetadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegiaoAfetada
        fields = '__all__'

class DoacaoSerializer(serializers.ModelSerializer):
    # Campos de leitura para mostrar o nome em vez de apenas o ID na resposta
    nome_destino = serializers.CharField(source='destino.nome_identificacao', read_only=True)

    class Meta:
        model = Doacao
        fields = [
            'id', 'produto', 'tipo', 'situacao', 'quantidade', 'unidade_medida', 'quantidade_por_volume',
            'destino', 'nome_destino',       # Mostra ID e Nome
            'data_doacao'
        ]