from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Voluntario, RegiaoAfetada, Doacao
from .serializers import VoluntarioSerializer, RegiaoAfetadaSerializer, DoacaoSerializer

# =================================================
# VOLUNTÁRIOS
# =================================================

@api_view(['GET', 'POST'])
def voluntario_lista(request):
    """
    Lista voluntário(os) ou cria um novo.
    """
    if request.method == 'GET':
        voluntarios = Voluntario.objects.all()
        
        # Filtros manuais (habilidade e disponibilidade)
        habilidade = request.query_params.get('habilidade')
        disponibilidade = request.query_params.get('disponibilidade')
        search = request.query_params.get('search') # Para simular o SearchFilter
        
        if habilidade:
            voluntarios = voluntarios.filter(habilidade_principal=habilidade)
        if disponibilidade:
            voluntarios = voluntarios.filter(disponibilidade=disponibilidade)
        if search:
            voluntarios = voluntarios.filter(
                Q(nome_completo__icontains=search) | 
                Q(cidade__icontains=search)
            )
            
        serializer = VoluntarioSerializer(voluntarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VoluntarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def voluntario_detalhes(request, pk):
    """
    Busca, atualiza ou deleta um voluntário específico (pelo ID/PK).
    """
    voluntario = get_object_or_404(Voluntario, pk=pk)

    if request.method == 'GET':
        serializer = VoluntarioSerializer(voluntario)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VoluntarioSerializer(voluntario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        voluntario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =================================================
# REGIÃO AFETADA
# =================================================

@api_view(['GET', 'POST'])
def regiao_lista(request):
    if request.method == 'GET':
        # Ordenação manual que antes estava no Meta
        regioes = RegiaoAfetada.objects.all().order_by('-nivel_prioridade', 'data_ocorrencia')
        serializer = RegiaoAfetadaSerializer(regioes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RegiaoAfetadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def regiao_detalhes(request, pk):
    regiao = get_object_or_404(RegiaoAfetada, pk=pk)

    if request.method == 'GET':
        serializer = RegiaoAfetadaSerializer(regiao)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegiaoAfetadaSerializer(regiao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        regiao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =================================================
# DOAÇÕES
# =================================================

@api_view(['GET', 'POST'])
def doacao_lista(request):
    if request.method == 'GET':
        doacoes = Doacao.objects.all()
        
        # Filtros manuais
        situacao = request.query_params.get('situacao')
        tipo = request.query_params.get('tipo')
        
        if situacao:
            doacoes = doacoes.filter(situacao=situacao)
        if tipo:
            doacoes = doacoes.filter(tipo=tipo)
            
        serializer = DoacaoSerializer(doacoes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def doacao_detalhes(request, pk):
    doacao = get_object_or_404(Doacao, pk=pk)

    if request.method == 'GET':
        serializer = DoacaoSerializer(doacao)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoacaoSerializer(doacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)