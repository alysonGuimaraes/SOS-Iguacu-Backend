from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

# Importa os modelos que serão testados
from .models import RegiaoAfetada, Voluntario, Doacao 

# --- Testes para o Model RegiaoAfetada ---
class RegiaoAfetadaModelTest(TestCase):
    """
    Testes unitários para o Model RegiaoAfetada.
    Foco em criação, __str__ e ordenação.
    """

    def setUp(self):
        """Cria instâncias básicas de RegiaoAfetada para uso em múltiplos testes."""
        
        # Cria a região de prioridade mais alta (Crítica) e data mais antiga
        self.regiao_critica_antiga = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro A - Crítico (Antigo)",
            cep="83000000", estado="PR", cidade="Rio Bonito", bairro="A", endereco="Rua X",
            tipo_desastre="Tornado", nivel_prioridade=4, status='AGUARDANDO',
            necessidades_imediatas="Resgate, Médicos",
            data_ocorrencia=timezone.now() - timedelta(days=2) # 2 dias atrás
        )
        
        # Cria a região de prioridade média (Danos Materiais)
        self.regiao_media = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro B - Médio",
            cep="83000001", estado="PR", cidade="Rio Bonito", bairro="B", endereco="Rua Y",
            tipo_desastre="Tornado", nivel_prioridade=2, status='EM_ATENDIMENTO',
            necessidades_imediatas="Cestas básicas",
            data_ocorrencia=timezone.now()
        )

        # Cria a região de prioridade alta (Desabrigados) e data mais recente
        self.regiao_alta_recente = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro C - Alta (Recente)",
            cep="83000002", estado="PR", cidade="Rio Bonito", bairro="C", endereco="Rua Z",
            tipo_desastre="Tornado", nivel_prioridade=3, status='AGUARDANDO',
            necessidades_imediatas="Lona, Água",
            data_ocorrencia=timezone.now() - timedelta(hours=1) # 1 hora atrás
        )

    def test_regiao_creation(self):
        """Verifica se a Região Afetada foi criada com sucesso."""
        self.assertEqual(RegiaoAfetada.objects.count(), 3)
        self.assertEqual(self.regiao_critica_antiga.estado, "PR")
        self.assertEqual(self.regiao_critica_antiga.nivel_prioridade, 4)
        self.assertEqual(self.regiao_media.get_status_display(), "Em Atendimento")

    def test_regiao_str_representation(self):
        """Verifica se o método __str__ retorna a string esperada."""
        # Espera: "Nome - Prioridade: Descrição da Prioridade"
        expected_str = f"{self.regiao_critica_antiga.nome_identificacao} - Prioridade: Crítica - Risco de Vida / Calamidade Pública"
        self.assertEqual(str(self.regiao_critica_antiga), expected_str)
    
    def test_ordering(self):
        """
        Verifica se a ordenação (Meta.ordering) está correta:
        - Primeiro por nivel_prioridade (decrescente: 4 > 3 > 2)
        - Segundo por data_ocorrencia (crescente, em caso de empate na prioridade)
        """
        regioes = RegiaoAfetada.objects.all()
        # A ordem esperada é 4 (critica) > 3 (alta) > 2 (media)
        
        self.assertEqual(regioes[0].nivel_prioridade, 4, "A primeira deve ser a Crítica (4)")
        self.assertEqual(regioes[1].nivel_prioridade, 3, "A segunda deve ser a Alta (3)")
        self.assertEqual(regioes[2].nivel_prioridade, 2, "A terceira deve ser a Média (2)")
        
        # Testando ordenação secundária (data_ocorrencia) em caso de empate na prioridade:
        # Criamos duas de prioridade 3 para testar a ordenação por data
        regiao_3_nova = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro D - Alta (Mais Nova)",
            cep="83000003", estado="PR", cidade="Rio Bonito", bairro="D", endereco="Rua T",
            tipo_desastre="Tornado", nivel_prioridade=3, status='AGUARDANDO',
            necessidades_imediatas="Roupas",
            data_ocorrencia=timezone.now() # A data mais recente
        )
        regiao_3_antiga = RegiaoAfetada.objects.create(
            nome_identificacao="Bairro E - Alta (Mais Antiga)",
            cep="83000004", estado="PR", cidade="Rio Bonito", bairro="E", endereco="Rua U",
            tipo_desastre="Tornado", nivel_prioridade=3, status='AGUARDANDO',
            necessidades_imediatas="Comida",
            data_ocorrencia=timezone.now() - timedelta(days=5) # A data mais antiga
        )
        
        # Rebuscando para testar a ordenação entre as de nível 3:
        regioes_nivel_3 = RegiaoAfetada.objects.filter(nivel_prioridade=3).order_by('-data_ocorrencia')
        
        # Esperamos que a 'regiao_3_antiga' venha antes da 'regiao_3_nova' (ordenação ascendente por data)
        self.assertEqual(regioes_nivel_3[0], regiao_3_antiga, "Região 3 mais antiga deve vir primeiro.")
        self.assertEqual(regioes_nivel_3[1], regiao_3_nova, "Região 3 mais nova deve vir depois.")


# --- Testes para o Model Voluntario ---
class VoluntarioModelTest(TestCase):
    """Testes unitários para o Model Voluntario."""

    def setUp(self):
        """Cria uma Região Afetada para ser destino do voluntário e um voluntário base."""
        self.regiao_destino = RegiaoAfetada.objects.create(
            nome_identificacao="Base de Apoio Principal",
            cep="00000000", estado="PR", cidade="Rio Bonito", bairro="Base", endereco="Rua Principal",
            tipo_desastre="Apoio", nivel_prioridade=1, necessidades_imediatas="Nenhuma"
        )
        
        self.voluntario_medico = Voluntario.objects.create(
            nome_completo="Dr. João da Silva",
            data_nascimento="1990-01-01",
            telefone="99887766", ddd="41",
            cidade="Curitiba", estado="PR",
            habilidade_principal='SAUDE',
            disponibilidade='TOTAL',
            regiao_afetada_atuacao=self.regiao_destino
        )
        
        self.voluntario_geral = Voluntario.objects.create(
            nome_completo="Maria de Souza",
            data_nascimento="1995-05-05",
            telefone="91234567", ddd="41",
            cidade="Curitiba", estado="PR",
            # Habilidade principal default 'GERAL' e disponibilidade default 'VARIAVEL'
        )

    def test_voluntario_creation_and_fields(self):
        """Verifica se o Voluntário foi criado com sucesso e seus campos estão corretos."""
        self.assertEqual(Voluntario.objects.count(), 2)
        self.assertEqual(self.voluntario_medico.cidade, "Curitiba")
        self.assertEqual(self.voluntario_medico.get_habilidade_principal_display(), "Profissional de Saúde (Médico/Enfermeiro)")
        self.assertEqual(self.voluntario_medico.regiao_afetada_atuacao, self.regiao_destino)
        
    def test_voluntario_defaults(self):
        """Verifica se os valores padrão são aplicados corretamente."""
        self.assertEqual(self.voluntario_geral.habilidade_principal, 'GERAL')
        self.assertEqual(self.voluntario_geral.disponibilidade, 'VARIAVEL')
        # regiao_afetada_atuacao deve ser NULL por padrão
        self.assertIsNone(self.voluntario_geral.regiao_afetada_atuacao)

    def test_voluntario_str_representation(self):
        """Verifica se o método __str__ retorna a string esperada."""
        # Espera: "Nome Completo (Descrição da Habilidade)"
        expected_str = "Dr. João da Silva (Profissional de Saúde (Médico/Enfermeiro))"
        self.assertEqual(str(self.voluntario_medico), expected_str)

# --- Testes para o Model Doacao ---
class DoacaoModelTest(TestCase):
    """Testes unitários para o Model Doacao."""
    
    def setUp(self):
        """Cria uma Região Afetada para ser destino da doação e uma doação base."""
        self.regiao_destino = RegiaoAfetada.objects.create(
            nome_identificacao="Base de Distribuição X",
            cep="00000000", estado="PR", cidade="Rio Bonito", bairro="Base", endereco="Rua Principal",
            tipo_desastre="Apoio", nivel_prioridade=1, necessidades_imediatas="Nenhuma"
        )
        
        self.doacao_agua = Doacao.objects.create(
            produto="Garrafas de Água 1.5L",
            tipo='AGUA',
            quantidade=100,
            unidade_medida='L',
            quantidade_por_volume=150, # 150 litros no total
            situacao='RESERVADO',
            destino=self.regiao_destino,
            entregue=False
        )
        
        self.doacao_estoque = Doacao.objects.create(
            produto="Arroz 5kg",
            tipo='ALIMENTO',
            quantidade=50,
            unidade_medida='KG',
            quantidade_por_volume=250, # 250 kg no total
            # destino é nulo, logo: Estoque Geral
        )

    def test_doacao_creation_and_fields(self):
        """Verifica se a Doação foi criada e salva com sucesso."""
        self.assertEqual(Doacao.objects.count(), 2)
        self.assertEqual(self.doacao_agua.produto, "Garrafas de Água 1.5L")
        self.assertEqual(self.doacao_agua.quantidade, 100)
        self.assertEqual(self.doacao_agua.destino, self.regiao_destino)
        self.assertEqual(self.doacao_estoque.situacao, 'DISPONIVEL', "O status default deve ser 'DISPONIVEL'.")

    def test_doacao_str_representation(self):
        """
        Verifica se o método __str__ retorna a string esperada.
        
        Nota: Este teste verifica se o nome de identificação do destino (ou 'Estoque Geral')
        está contido na representação em string.
        """
        
        # Testamos o valor do 'destino'.
        destino_nome_agua = self.doacao_agua.destino.nome_identificacao
        self.assertIn(destino_nome_agua, str(self.doacao_agua))

        destino_nome_estoque = 'Estoque Geral'
        self.assertIn(destino_nome_estoque, str(self.doacao_estoque))

    def test_doacao_defaults(self):
        """Verifica se os valores padrão são aplicados corretamente."""
        self.assertEqual(self.doacao_estoque.tipo, 'ALIMENTO')
        self.assertEqual(self.doacao_estoque.quantidade, 50)
        self.assertIsNone(self.doacao_estoque.destino)
        self.assertFalse(self.doacao_estoque.entregue)