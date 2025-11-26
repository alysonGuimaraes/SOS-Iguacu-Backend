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


class CepInputSerializer(serializers.Serializer):
    # Define que o campo é texto, com tamanho min/max básico
    cep = serializers.CharField(min_length=8, max_length=9)

    def validate_cep(self, value):
        clean_value = value.replace('-', '').replace('.', '')

        if not clean_value.isdigit():
            raise serializers.ValidationError("O CEP deve conter apenas números.")

        if len(clean_value) != 8:
            raise serializers.ValidationError("O CEP deve ter exatamente 8 dígitos numéricos.")

        return clean_value