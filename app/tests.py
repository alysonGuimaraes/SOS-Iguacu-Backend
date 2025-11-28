# Create your tests here.

from unittest.mock import Mock, patch
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

# Importa os modelos e serializers
from .models import RegiaoAfetada, Voluntario, Doacao
from .serializers import GeoInputSerializer, CepInputSerializer, VoluntarioSerializer, RegiaoAfetadaSerializer, DoacaoSerializer


# ==============================================================================
# 1. TESTES UNITÁRIOS DOS MODELS (Model Tests)
# (Baseado e complementado a partir de models_tests.py)
# ==============================================================================

class RegiaoAfetadaModelTest(TestCase):
    """
    Testes unitários para o Model RegiaoAfetada.
    Foco em criação, __str__, choices e ordenação.
    """

    def setUp(self):
        """Cria instâncias básicas de RegiaoAfetada para uso em múltiplos testes."""
        self.regiao_critica_antiga = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro A - Crítico (Antigo)",
            cep="83000000", estado="PR", cidade="Rio Bonito", bairro="A", endereco="Rua X",
            tipo_desastre="Tornado", nivel_prioridade=4, status='AGUARDANDO',
            necessidades_imediatas="Resgate, Médicos",
            data_ocorrencia=timezone.now() - timedelta(days=2)
        )
        self.regiao_media = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro B - Médio",
            cep="83000001", estado="PR", cidade="Rio Bonito", bairro="B", endereco="Rua Y",
            tipo_desastre="Tornado", nivel_prioridade=2, status='EM_ATENDIMENTO',
            necessidades_imediatas="Cestas básicas",
            data_ocorrencia=timezone.now()
        )
        self.regiao_alta_recente = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro C - Alta (Recente)",
            cep="83000002", estado="PR", cidade="Rio Bonito", bairro="C", endereco="Rua Z",
            tipo_desastre="Tornado", nivel_prioridade=3, status='AGUARDANDO',
            necessidades_imediatas="Lona, Água",
            data_ocorrencia=timezone.now() - timedelta(hours=1)
        )

    def test_regiao_creation_and_status_choices(self):
        """Verifica se a Região Afetada foi criada e cobre todos os STATUS_CHOICES."""
        self.assertEqual(RegiaoAfetada.objects.count(), 3)
        self.assertEqual(self.regiao_media.get_status_display(), "Em Atendimento")

        # Testa o status CONCLUIDO (para cobertura)
        regiao_concluida = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro D - Concluído",
            cep="83000003", estado="PR", cidade="Rio Bonito", bairro="D", endereco="Rua W",
            tipo_desastre="Tornado", nivel_prioridade=1, status='CONCLUIDO',
            necessidades_imediatas="Nenhuma"
        )
        self.assertEqual(regiao_concluida.status, 'CONCLUIDO')
        self.assertEqual(regiao_concluida.get_status_display(), "Situação Estabilizada")


    def test_regiao_str_representation(self):
        """Verifica se o método __str__ retorna a string esperada."""
        expected_str = f"{self.regiao_critica_antiga.nome_identificacao} - Prioridade: Crítica - Risco de Vida / Calamidade Pública"
        self.assertEqual(str(self.regiao_critica_antiga), expected_str)
    
    def test_ordering(self):
        """Verifica se a ordenação (Meta.ordering: -nivel_prioridade, data_ocorrencia) está correta."""
        regioes = RegiaoAfetada.objects.all()
        # Ordem esperada: 4 (critica) > 3 (alta) > 2 (media)
        self.assertEqual(regioes[0].nivel_prioridade, 4)
        self.assertEqual(regioes[1].nivel_prioridade, 3)
        self.assertEqual(regioes[2].nivel_prioridade, 2)


class VoluntarioModelTest(TestCase):
    """Testes unitários para o Model Voluntario, focando na cobertura de Choices."""

    def setUp(self):
        self.regiao_destino = RegiaoAfetada.objects.create(
            nome_identificacao="Base de Apoio Principal",
            cep="00000000", estado="PR", cidade="Rio Bonito", bairro="Base", endereco="Rua Principal",
            tipo_desastre="Apoio", nivel_prioridade=1, necessidades_imediatas="Nenhuma"
        )
        self.data_nasc = date(1990, 1, 1)

    def test_voluntario_all_choices_coverage(self):
        """Cobre o restante das HABILIDADES_CHOICES e DISPONIBILIDADE_CHOICES."""
        
        # Cria voluntário com Habilidades e Disponibilidades não testadas
        self.voluntario_logistica = Voluntario.objects.create(
            nome_completo="José Logística", data_nascimento=self.data_nasc,
            telefone="91111111", ddd="41", cidade="CWB", estado="PR",
            habilidade_principal='LOGISTICA', disponibilidade='MANHA'
        )
        self.voluntario_resgate = Voluntario.objects.create(
            nome_completo="Ana Resgate", data_nascimento=self.data_nasc,
            telefone="92222222", ddd="41", cidade="CWB", estado="PR",
            habilidade_principal='RESGATE', disponibilidade='TARDE'
        )
        self.voluntario_psico = Voluntario.objects.create(
            nome_completo="Pedro Psico", data_nascimento=self.data_nasc,
            telefone="93333333", ddd="41", cidade="CWB", estado="PR",
            habilidade_principal='PSICO', disponibilidade='NOITE'
        )
        self.voluntario_cozinha = Voluntario.objects.create(
            nome_completo="Mari Cozinha", data_nascimento=self.data_nasc,
            telefone="94444444", ddd="41", cidade="CWB", estado="PR",
            habilidade_principal='COZINHA', disponibilidade='MADRUGADA'
        )
        self.voluntario_fim_semana = Voluntario.objects.create(
            nome_completo="Fim de Semana", data_nascimento=self.data_nasc,
            telefone="95555555", ddd="41", cidade="CWB", estado="PR",
            habilidade_principal='GERAL', disponibilidade='FIM_SEMANA'
        )

        self.assertEqual(self.voluntario_logistica.get_habilidade_principal_display(), "Logística e Transporte")
        self.assertEqual(self.voluntario_resgate.get_disponibilidade_display(), "Tarde (13:00 - 18:00)")
        self.assertEqual(self.voluntario_cozinha.get_disponibilidade_display(), "Madrugada (22:00 - 08:00)")
        self.assertEqual(self.voluntario_fim_semana.disponibilidade, 'FIM_SEMANA')


    def test_voluntario_str_representation(self):
        """Verifica se o método __str__ retorna a string esperada."""
        voluntario = Voluntario.objects.create(
            nome_completo="Dr. João da Silva", data_nascimento=self.data_nasc,
            telefone="99887766", ddd="41", cidade="Curitiba", estado="PR",
            habilidade_principal='SAUDE', disponibilidade='TOTAL'
        )
        expected_str = "Dr. João da Silva (Profissional de Saúde (Médico/Enfermeiro))"
        self.assertEqual(str(voluntario), expected_str)


class DoacaoModelTest(TestCase):
    """Testes unitários para o Model Doacao, focando na cobertura de Choices."""
    
    def setUp(self):
        self.regiao_destino = RegiaoAfetada.objects.create(
            nome_identificacao="Base de Distribuição X",
            cep="00000000", estado="PR", cidade="Rio Bonito", bairro="Base", endereco="Rua Principal",
            tipo_desastre="Apoio", nivel_prioridade=1, necessidades_imediatas="Nenhuma"
        )
        self.doacao_estoque = Doacao.objects.create(
            produto="Arroz 5kg", tipo='ALIMENTO', quantidade=50,
        )

    def test_doacao_all_choices_coverage(self):
        """Cobre o restante dos TIPO_ITEM e SITUACAO_CHOICES."""

        # Cobre os tipos de item não testados
        Doacao.objects.create(produto="Kit Higiene", tipo='HIGIENE', quantidade=10, unidade_medida='UN')
        Doacao.objects.create(produto="Dinheiro", tipo='DINHEIRO', quantidade=1000, unidade_medida='UN')
        Doacao.objects.create(produto="Cimento", tipo='MATERIAL', quantidade=20, unidade_medida='CX')
        Doacao.objects.create(produto="Paracetamol", tipo='MEDICAMENTO', quantidade=50, unidade_medida='UN')
        Doacao.objects.create(produto="Camisetas", tipo='ROUPA', quantidade=200, unidade_medida='UN')

        # Cobre os status de situação restantes
        doacao_em_transito = Doacao.objects.create(
            produto="Barco", tipo='OUTRO', quantidade=1, situacao='EM_TRANSITO', destino=self.regiao_destino
        )
        doacao_entregue = Doacao.objects.create(
            produto="Ração", tipo='ALIMENTO', quantidade=50, situacao='ENTREGUE', entregue=True
        )

        self.assertEqual(doacao_em_transito.get_situacao_display(), "Em Trânsito / Saiu para Entrega")
        self.assertEqual(doacao_entregue.get_situacao_display(), "Entregue ao Destino")
        self.assertTrue(doacao_entregue.entregue)
        
    def test_doacao_str_representation(self):
        """Verifica o __str__ para destino nulo e não nulo."""
        
        # Destino nulo (Estoque Geral)
        self.doacao_estoque.destino = None
        self.doacao_estoque.save()
        self.assertIn('Estoque Geral', str(self.doacao_estoque))

        # Destino não nulo
        doacao_agua = Doacao.objects.create(
            produto="Garrafas de Água", tipo='AGUA', quantidade=100, destino=self.regiao_destino
        )
        self.assertIn(self.regiao_destino.nome_identificacao, str(doacao_agua))


# ==============================================================================
# 2. TESTES DE ENDPOINTS DA API (View Tests)
# ==============================================================================

class VoluntarioAPITest(APITestCase):
    """Testes para os endpoints de Voluntário."""
    
    def setUp(self):
        self.client = APIClient()
        self.url_lista = reverse('voluntario_lista')
        self.data_nasc = date(1990, 1, 1).strftime('%Y-%m-%d')
        
        # Cria voluntários para teste de filtros
        self.v1 = Voluntario.objects.create(
            nome_completo="João Geral Silva", data_nascimento=self.data_nasc,
            telefone="90000001", ddd="41", cidade="Curitiba", estado="PR",
            habilidade_principal='GERAL', disponibilidade='MANHA'
        )
        self.v2 = Voluntario.objects.create(
            nome_completo="Maria Saude Souza", data_nascimento=self.data_nasc,
            telefone="90000002", ddd="41", cidade="Pinhais", estado="PR",
            habilidade_principal='SAUDE', disponibilidade='TARDE'
        )
        self.v3_saude = Voluntario.objects.create(
            nome_completo="Carlos Saude", data_nascimento=self.data_nasc,
            telefone="90000003", ddd="41", cidade="Curitiba", estado="PR",
            habilidade_principal='SAUDE', disponibilidade='MANHA'
        )
        
        self.voluntario_data = {
            'nome_completo': 'Novo Voluntário', 
            'data_nascimento': '2000-10-10', 
            'telefone': '98765432', 
            'ddd': '11', 
            'cidade': 'São Paulo', 
            'estado': 'SP',
            'habilidade_principal': 'LOGISTICA',
            'disponibilidade': 'TOTAL'
        }

    # Testes GET (Listagem e Filtros)
    def test_list_voluntarios(self):
        response = self.client.get(self.url_lista)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_habilidade(self):
        response = self.client.get(self.url_lista, {'habilidade': 'SAUDE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        self.assertTrue(all(v['habilidade_principal'] == 'SAUDE' for v in response.data))

    def test_filter_by_disponibilidade(self):
        response = self.client.get(self.url_lista, {'disponibilidade': 'MANHA'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(v['disponibilidade'] == 'MANHA' for v in response.data))

    def test_search_filter(self):
        # Busca por nome
        response_nome = self.client.get(self.url_lista, {'search': 'Silva'})
        self.assertEqual(response_nome.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_nome.data), 1)

        # Busca por cidade
        response_cidade = self.client.get(self.url_lista, {'search': 'Curitiba'})
        self.assertEqual(response_cidade.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_cidade.data), 2)
        
    # Teste POST (Criação)
    def test_create_voluntario_success(self):
        response = self.client.post(self.url_lista, self.voluntario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voluntario.objects.count(), 4)
        self.assertEqual(response.data['nome_completo'], 'Novo Voluntário')

    def test_create_voluntario_fail(self):
        invalid_data = self.voluntario_data.copy()
        invalid_data.pop('nome_completo')
        response = self.client.post(self.url_lista, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome_completo', response.data)

    # Testes de Detalhes (GET, PUT, DELETE)
    def test_retrieve_voluntario(self):
        url_detalhes = reverse('voluntario_detalhes', args=[self.v1.id])
        response = self.client.get(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_completo'], self.v1.nome_completo)

    def test_update_voluntario(self):
        url_detalhes = reverse('voluntario_detalhes', args=[self.v1.id])
        updated_data = {'habilidade_principal': 'RESGATE'}
        data_completa = VoluntarioSerializer(self.v1).data
        data_completa.update(updated_data)

        response = self.client.put(url_detalhes, data_completa, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.v1.refresh_from_db()
        self.assertEqual(self.v1.habilidade_principal, 'RESGATE')

    def test_delete_voluntario(self):
        url_detalhes = reverse('voluntario_detalhes', args=[self.v1.id])
        response = self.client.delete(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Voluntario.objects.count(), 2)


class RegiaoAfetadaAPITest(APITestCase):
    """Testes para os endpoints de Região Afetada."""

    def setUp(self):
        self.client = APIClient()
        self.url_lista = reverse('regiao_lista')
        
        # Regiões para teste de ordenação
        self.r1_alta = RegiaoAfetada.objects.create(
            nome_identificacao="R1 - Alta", cep="10000000", estado="PR", cidade="Rio B.", bairro="A", endereco="Rua X",
            tipo_desastre="Enchente", nivel_prioridade=3, necessidades_imediatas="Lona", status='AGUARDANDO',
            data_ocorrencia=timezone.now() - timedelta(hours=2)
        )
        self.r2_critica = RegiaoAfetada.objects.create(
            nome_identificacao="R2 - Crítica", cep="20000000", estado="PR", cidade="Rio B.", bairro="B", endereco="Rua Y",
            tipo_desastre="Tornado", nivel_prioridade=4, necessidades_imediatas="Resgate", status='AGUARDANDO',
            data_ocorrencia=timezone.now() - timedelta(hours=1)
        )
        self.r3_baixa = RegiaoAfetada.objects.create(
            nome_identificacao="R3 - Baixa", cep="30000000", estado="PR", cidade="Rio B.", bairro="C", endereco="Rua Z",
            tipo_desastre="Alagamento", nivel_prioridade=1, necessidades_imediatas="Monitoramento", status='CONCLUIDO',
            data_ocorrencia=timezone.now()
        )
        
        self.regiao_data = {
            'nome_identificacao': 'Nova Região Teste', 
            'cep': '83060035', 
            'estado': 'PR', 
            'cidade': 'Rio Bonito', 
            'bairro': 'Centro', 
            'endereco': 'Rua Teste',
            'tipo_desastre': 'Incêndio', 
            'nivel_prioridade': 2, 
            'status': 'EM_ATENDIMENTO',
            'necessidades_imediatas': 'Bombeiros, Água'
        }

    # Testes GET (Listagem e Ordenação)
    def test_list_regioes_and_ordering(self):
        """Verifica se a listagem retorna o status 200 e a ordenação correta (-prioridade, +data)."""
        response = self.client.get(self.url_lista)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve estar ordenado por: Crítica (4) > Alta (3) > Baixa (1)
        self.assertEqual(response.data[0]['nome_identificacao'], self.r2_critica.nome_identificacao)
        self.assertEqual(response.data[1]['nome_identificacao'], self.r1_alta.nome_identificacao)
        self.assertEqual(response.data[2]['nome_identificacao'], self.r3_baixa.nome_identificacao)

    # Teste POST (Criação)
    def test_create_regiao_success(self):
        response = self.client.post(self.url_lista, self.regiao_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegiaoAfetada.objects.count(), 4)

    # Testes de Detalhes (GET, PUT, DELETE)
    def test_retrieve_regiao(self):
        url_detalhes = reverse('regiao_detalhes', args=[self.r1_alta.id])
        response = self.client.get(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nivel_prioridade'], 3)

    def test_update_regiao(self):
        url_detalhes = reverse('regiao_detalhes', args=[self.r1_alta.id])
        updated_data = {'status': 'CONCLUIDO'}
        data_completa = RegiaoAfetadaSerializer(self.r1_alta).data
        data_completa.update(updated_data)

        response = self.client.put(url_detalhes, data_completa, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.r1_alta.refresh_from_db()
        self.assertEqual(self.r1_alta.status, 'CONCLUIDO')

    def test_delete_regiao(self):
        url_detalhes = reverse('regiao_detalhes', args=[self.r1_alta.id])
        response = self.client.delete(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RegiaoAfetada.objects.count(), 2)


class DoacaoAPITest(APITestCase):
    """Testes para os endpoints de Doação, focando em Filtros."""
    
    def setUp(self):
        self.client = APIClient()
        self.url_lista = reverse('doacao_lista')
        
        # Região destino para as doações
        self.regiao = RegiaoAfetada.objects.create(
            nome_identificacao="Posto de Ajuda", cep="10000000", estado="PR", cidade="Rio B.", bairro="A", endereco="Rua X",
            tipo_desastre="Enchente", nivel_prioridade=3, necessidades_imediatas="Lona", status='AGUARDANDO'
        )
        
        # Doações para teste de filtros
        self.d1 = Doacao.objects.create(produto="Água 500ml", tipo='AGUA', quantidade=100, situacao='DISPONIVEL')
        self.d2 = Doacao.objects.create(produto="Arroz 1kg", tipo='ALIMENTO', quantidade=50, situacao='RESERVADO', destino=self.regiao)
        self.d3 = Doacao.objects.create(produto="Cobertor", tipo='ROUPA', quantidade=20, situacao='DISPONIVEL')
        self.d4 = Doacao.objects.create(produto="Kit Médico", tipo='MEDICAMENTO', quantidade=5, situacao='EM_TRANSITO', destino=self.regiao)
        
        self.doacao_data = {
            'produto': 'Marmitex', 'tipo': 'ALIMENTO', 'quantidade': 150, 
            'unidade_medida': 'UN', 'quantidade_por_volume': 150,
            'situacao': 'DISPONIVEL', 'destino': str(self.regiao.id)
        }

    # Testes GET (Listagem e Filtros)
    def test_list_doacoes(self):
        response = self.client.get(self.url_lista)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_by_situacao(self):
        response = self.client.get(self.url_lista, {'situacao': 'DISPONIVEL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        response_transito = self.client.get(self.url_lista, {'situacao': 'EM_TRANSITO'})
        self.assertEqual(len(response_transito.data), 1)

    def test_filter_by_tipo(self):
        response = self.client.get(self.url_lista, {'tipo': 'ALIMENTO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Teste POST (Criação)
    def test_create_doacao_success(self):
        response = self.client.post(self.url_lista, self.doacao_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doacao.objects.count(), 5)
        self.assertEqual(response.data['nome_destino'], self.regiao.nome_identificacao)

    # Testes de Detalhes (GET, PUT, DELETE)
    def test_retrieve_doacao(self):
        url_detalhes = reverse('doacao_detalhes', args=[self.d2.id])
        response = self.client.get(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['produto'], self.d2.produto)

    def test_update_doacao_status(self):
        url_detalhes = reverse('doacao_detalhes', args=[self.d2.id])
        updated_data = {'situacao': 'ENTREGUE', 'entregue': True}
        data_completa = DoacaoSerializer(self.d2).data
        data_completa.update(updated_data)

        response = self.client.put(url_detalhes, data_completa, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.d2.refresh_from_db()
        self.assertEqual(self.d2.situacao, 'ENTREGUE')
        self.assertTrue(self.d2.entregue)

    def test_delete_doacao(self):
        url_detalhes = reverse('doacao_detalhes', args=[self.d1.id])
        response = self.client.delete(url_detalhes)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Doacao.objects.count(), 3)


# ==============================================================================
# 3. TESTE DE INTEGRAÇÃO (Integration Test)
# ==============================================================================

class IntegrationTest(APITestCase):
    """
    Testa o fluxo completo:
    1. Cria uma Região Afetada (destino).
    2. Cria um Voluntário para essa região.
    3. Cria uma Doação para essa região.
    4. Verifica se a Doação lista o nome da Região (via Serializer/Foreign Key).
    """

    def setUp(self):
        self.client = APIClient()
        self.url_regiao = reverse('regiao_lista')
        self.url_voluntario = reverse('voluntario_lista')
        self.url_doacao = reverse('doacao_lista')

    def test_complete_relief_flow(self):
        # 1. POST: Criar Região Afetada (Base de Atendimento)
        regiao_data = {
            'nome_identificacao': 'Base de Resgate Integrada', 
            'cep': '99999999', 
            'estado': 'SC', 
            'cidade': 'Florianópolis', 
            'bairro': 'Centro', 
            'endereco': 'Rua do Resgate',
            'tipo_desastre': 'Incêndio', 
            'nivel_prioridade': 4, 
            'status': 'AGUARDANDO',
            'necessidades_imediatas': 'Tudo'
        }
        response_regiao = self.client.post(self.url_regiao, regiao_data, format='json')
        self.assertEqual(response_regiao.status_code, status.HTTP_201_CREATED)
        regiao_id = response_regiao.data['id']
        regiao_nome = response_regiao.data['nome_identificacao']

        # 2. POST: Criar Voluntário ligado à nova região
        voluntario_data = {
            'nome_completo': 'Voluntário de Resgate', 
            'data_nascimento': '1985-01-01', 
            'telefone': '99123456', 
            'ddd': '48', 
            'cidade': 'Florianópolis', 
            'estado': 'SC',
            'habilidade_principal': 'RESGATE',
            'disponibilidade': 'TOTAL',
            'regiao_afetada_atuacao': regiao_id # Liga o voluntário à região
        }
        response_voluntario = self.client.post(self.url_voluntario, voluntario_data, format='json')
        self.assertEqual(response_voluntario.status_code, status.HTTP_201_CREATED)
        
        # 3. POST: Criar Doação reservada para a nova região
        doacao_data = {
            'produto': 'Roupas de Cama', 
            'tipo': 'ROUPA', 
            'quantidade': 200, 
            'unidade_medida': 'UN', 
            'quantidade_por_volume': 200,
            'situacao': 'RESERVADO',
            'destino': regiao_id # Liga a doação à região
        }
        response_doacao = self.client.post(self.url_doacao, doacao_data, format='json')
        self.assertEqual(response_doacao.status_code, status.HTTP_201_CREATED)
        doacao_id = response_doacao.data['id']
        
        # 4. GET: Verificar se a doação mostra o nome da região (Serialização da FK)
        url_doacao_detalhes = reverse('doacao_detalhes', args=[doacao_id])
        response_check = self.client.get(url_doacao_detalhes)
        self.assertEqual(response_check.status_code, status.HTTP_200_OK)
        
        # O campo 'nome_destino' no serializer deve ser preenchido
        self.assertEqual(response_check.data['nome_destino'], regiao_nome) 
        self.assertEqual(response_check.data['situacao'], 'RESERVADO')
        
        # 5. PUT: Atualizar o status da Doação para 'ENTREGUE'
        update_data = response_check.data.copy()
        update_data['situacao'] = 'ENTREGUE'
        update_data['entregue'] = True

        response_update = self.client.put(url_doacao_detalhes, update_data, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data['situacao'], 'ENTREGUE')
        self.assertTrue(response_update.data['entregue'])

        # Fim do fluxo de integração com sucesso

# ==============================================================================
# 4. TESTE DE APIs EXTERNAS
# ==============================================================================

class CepValidationTest(TestCase):
    """
    Testa apenas se as regras de validação (Serializer) estão funcionando.
    Não envolve chamadas externas.
    """
    
    def test_cep_valido_com_formatacao(self):
        # Cenário: Usuário manda CEP com ponto e traço
        data = {'cep': '12345-678'}
        serializer = CepInputSerializer(data=data)
        
        # O serializer deve aceitar
        self.assertTrue(serializer.is_valid())
        # E deve limpar os caracteres especiais
        self.assertEqual(serializer.validated_data['cep'], '12345678')

    def test_cep_invalido_letras(self):
        # Cenário: Usuário manda letras
        data = {'cep': '1234567a'}
        serializer = CepInputSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('cep', serializer.errors) # Deve ter erro no campo 'cep'

    def test_cep_invalido_tamanho(self):
        # Cenário: CEP curto demais
        data = {'cep': '123'}
        serializer = CepInputSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())


class CepIntegrationTest(TestCase):
    """
    Testa a View e a integração com a 'libs', mas MOCKANDO o requests.
    """
    
    def setUp(self):
        self.client = APIClient()

    # O @patch substitui o 'requests.get' VERDADEIRO por um FALSO apenas neste teste
    @patch('app.services.viacep.requests.get')
    def test_consulta_cep_sucesso(self, mock_get):
        """
        Simula uma chamada onde o ViaCep retorna sucesso (200).
        """
        # 1. Configurar o Dublê (Mock)
        resposta_simulada = Mock()
        resposta_simulada.status_code = 200
        # O json() que o requests retornaria:
        resposta_simulada.json.return_value = {
            "cep": "01001-000",
            "bairro": "teste",
            "logradouro": "Praça da Sé",
            "localidade": "São Paulo",
            "uf": "SP"
        }
        # Dizemos ao mock_get para retornar nossa resposta simulada
        mock_get.return_value = resposta_simulada

        # 2. Fazer a requisição na NOSSA View
        # Use o 'name' que definimos no urls.py
        url = reverse('busca-cep', args=['01001000']) 
        response = self.client.get(url)

        # 3. Asserts
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['cidade'], 'São Paulo')

    @patch('app.services.viacep.requests.get')
    def test_consulta_cep_inexistente(self, mock_get):
        """
        Simula o cenário onde o CEP tem formato válido, mas não existe no ViaCep.
        """
        resposta_simulada = Mock()
        resposta_simulada.status_code = 200
        # O ViaCep retorna erro=True quando não acha
        resposta_simulada.json.return_value = {"erro": True}
        
        mock_get.return_value = resposta_simulada

        url = reverse('busca-cep', args=['99999999'])
        response = self.client.get(url)

        # Nossa view deve retornar 400 Bad Request nesse caso
        self.assertEqual(response.status_code, 400)
        self.assertIn('erro', response.data)


class GeoValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('geo-reversa')

    def test_coordenadas_validas(self):
        """Testa se o serializer aceita coordenadas reais."""
        valid_payload = {
            "latitude": -23.5505,
            "longitude": -46.6333
        }
        resposta_fake = Mock()
        resposta_fake.status_code = 200
        resposta_fake.json.return_value = {
            "place_id": 123456,
            "lat": "-23.55052",
            "lon": "-46.63330",
            "display_name": "Praça da Sé, Sé, São Paulo, SP, Brasil",
            "address": {
                "road": "Praça da Sé",
                "house_number": "S/N",
                "suburb": "Sé",
                "town": "São Paulo",
                "state": "São Paulo",
                "country": "Brasil",
                "postcode": "01001-000"
            }
        }

        response = self.client.get(self.url, valid_payload)

        self.assertEqual(response.status_code, 200)

    def test_latitude_impossivel(self):
        """Deve barrar latitudes fora de -90 a +90"""
        payload = {
            "latitude": 95.0, # Inválido
            "longitude": -46.6333
        }
        response = self.client.get(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('latitude', response.data) # O erro deve estar no campo latitude

    def test_longitude_impossivel(self):
        """Deve barrar longitudes fora de -180 a +180"""
        payload = {
            "latitude": -23.55,
            "longitude": -200.0 # Inválido
        }
        response = self.client.get(self.url, payload, format='json')
        self.assertEqual(response.status_code, 400)


class GeoIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('geo-reversa')
        self.valid_payload = {
            "latitude": -23.55052,
            "longitude": -46.63330
        }

    # Mockamos o requests.get lá dentro da lib do OpenStreetMap
    @patch('app.services.openstreetmap.requests.get')
    def test_geo_reversa_sucesso(self, mock_get):
        """
        Simula uma resposta de sucesso do OpenStreetMap.
        """
        # 1. Preparar o Mock (O que a API retornaria na vida real)
        resposta_fake = Mock()
        resposta_fake.status_code = 200
        resposta_fake.json.return_value = {
            "place_id": 123456,
            "lat": "-23.55052",
            "lon": "-46.63330",
            "display_name": "Praça da Sé, Sé, São Paulo, SP, Brasil",
            "address": {
                "road": "Praça da Sé",
                "house_number": "S/N",
                "suburb": "Sé",
                "town": "São Paulo",
                "state": "São Paulo",
                "country": "Brasil",
                "postcode": "01001-000"
            }
        }
        mock_get.return_value = resposta_fake

        # 2. Ação
        response = self.client.get(self.url, self.valid_payload)

        # 3. Asserts
        self.assertEqual(response.status_code, 200)
        
        # Verifica se nossa API formatou os dados corretamente (DTO)
        self.assertEqual(response.data['rua'], "Praça da Sé")
        self.assertEqual(response.data['cidade'], "São Paulo")
        
        # Verifica se o cache foi chamado (se você já tiver implementado o cache)
        # mock_get.assert_called_once() 

    @patch('app.services.openstreetmap.requests.get')
    def test_geo_reversa_falha_api(self, mock_get):
        """
        Simula erro 500 ou indisponibilidade do OpenStreetMap.
        """
        # O mock lança uma exceção de timeout/conexão
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Timeout")

        response = self.client.get(self.url, self.valid_payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    @patch('app.services.openstreetmap.requests.get')
    def test_geo_local_nao_encontrado(self, mock_get):
        """
        Simula coordenadas no meio do oceano (sem endereço).
        """
        resposta_fake = Mock()
        resposta_fake.status_code = 200
        # Nominatim às vezes retorna 'error' no JSON quando não acha
        resposta_fake.json.return_value = {"error": "Unable to geocode"}
        
        mock_get.return_value = resposta_fake

        response = self.client.get(self.url, self.valid_payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Não foi possível realizar a geolocalização reversa")

    @patch('app.services.openstreetmap.requests.get')
    def test_geo_dados_endereco_nao_encontrado(self, mock_get):
        """
        Simula um retorno positivo da geolocalização, porém sem dados de endereço disponíveis
        """
        resposta_fake = Mock()
        resposta_fake.status_code = 200
        # Nominatim às vezes retorna 'error' no JSON quando não acha
        resposta_fake.json.return_value = {
            "place_id": 123456,
            "lat": "-23.55052",
            "lon": "-46.63330",
            "display_name": "São Paulo, SP, Brasil",
            "address": {
            }
        }
        
        mock_get.return_value = resposta_fake

        response = self.client.get(self.url, self.valid_payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Não foi possível encontrar informações de endereço para as coordenadas inseridas")
