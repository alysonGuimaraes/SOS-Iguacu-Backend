# views.py (no seu app 'core')
from rest_framework import viewsets, status
from rest_framework.response import Response 
from .models import RegiaoAfetada
from .serializers import RegiaoAfetadaSerializer
# IMPORTAÇÃO ATUALIZADA:
from .BuscaCEP import buscar_endereco_por_cep # <- AQUI ESTÁ A MUDANÇA

# ... (restante do código da classe RegiaoAfetadaViewSet permanece o mesmo)

class RegiaoAfetadaViewSet(viewsets.ModelViewSet):
    """API endpoint para Regiões Afetadas com preenchimento via CEP."""
    queryset = RegiaoAfetada.objects.all()
    serializer_class = RegiaoAfetadaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        cep = data.get('cep')
        
        # 1. Busca os dados de endereço
        endereco_data = buscar_endereco_por_cep(cep) # Usa a função importada

        if not endereco_data:
            return Response(
                {"error": "CEP inválido ou erro na consulta de endereço."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Atualiza os dados de entrada com as informações obtidas
        data['endereco'] = endereco_data.get('endereco')
        data['bairro'] = endereco_data.get('bairro')
        data['cidade'] = 'Rio Bonito do Iguaçu'
        data['cep'] = endereco_data.get('cep_formatado')
        
        # 3. Passa os dados atualizados para o Serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
