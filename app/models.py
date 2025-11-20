from django.db import models
from uuid import uuid4

class RegiaoAfetada(models.Model):
    """
    Representa o local do desastre.
    Foco: Priorização e Status.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    NIVEL_GRAVIDADE = [
        (1, 'Baixa - Monitoramento'),
        (2, 'Média - Danos Materiais'),
        (3, 'Alta - Desabrigados'),
        (4, 'Crítica - Risco de Vida / Calamidade Pública'),
    ]
    
    STATUS_CHOICES = [
        ('AGUARDANDO', 'Aguardando Ajuda'),
        ('EM_ATENDIMENTO', 'Em Atendimento'),
        ('CONCLUIDO', 'Situação Estabilizada'),
    ]

    nome_identificacao = models.CharField(max_length=100, help_text="Ex: Bairro Centro - Enchente 2024")
    
    # Endereçamento
    cep = models.CharField(max_length=8, help_text="CEP no formato apenas com números Ex.: '83060-035' -> '83060035'")
    estado = models.CharField(max_length=2, help_text="Ex: PR, SP, RJ, BA")
    cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100, verbose_name="Rua/Logradouro")
    
    # Campos de Gestão de Crise
    tipo_desastre = models.CharField(max_length=100, help_text="Ex: Alagamento, Deslizamento, Incêndio")
    nivel_prioridade = models.IntegerField(choices=NIVEL_GRAVIDADE, default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGUARDANDO')
    
    # Descrição das necessidades específicas daquela região
    necessidades_imediatas = models.TextField(help_text="O que é mais urgente? Água? Barcos? Médicos?")
    
    data_ocorrencia = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-nivel_prioridade', 'data_ocorrencia'] # Ordena automaticamente do mais crítico para o menos crítico

    def __str__(self):
        return f"{self.nome_identificacao} - Prioridade: {self.get_nivel_prioridade_display()}"

class Voluntario(models.Model):
    """
    Representa uma pessoa disposta a ajudar.
    Foco: Habilidades e Contato.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    HABILIDADES_CHOICES = [
        ('SAUDE', 'Profissional de Saúde (Médico/Enfermeiro)'),
        ('RESGATE', 'Busca e Resgate'),
        ('LOGISTICA', 'Logística e Transporte'),
        ('PSICO', 'Apoio Psicológico'),
        ('GERAL', 'Serviços Gerais / Limpeza'),
        ('COZINHA', 'Cozinha e Alimentação'),
    ]

    DISPONIBILIDADE_CHOICES = [
        ('MANHA', 'Manhã (08:00 - 12:00)'),
        ('TARDE', 'Tarde (13:00 - 18:00)'),
        ('NOITE', 'Noite (19:00 - 22:00)'),
        ('MADRUGADA', 'Madrugada (22:00 - 08:00)'),
        ('FIM_SEMANA', 'Finais de Semana'),
        ('TOTAL', 'Disponibilidade Total'),
        ('VARIAVEL', 'Horário Variável / A combinar'),
    ]

    # Informações básicas do voluntário
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    
    # Contato é crucial em emergências
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=9, help_text="Celular ou telefone de contato")
    ddd = models.CharField(max_length=2)
    
    # Localização do voluntário (para saber se ele está perto da região afetada)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    # Habilidade principal ajuda a direcionar o voluntário certo para a necessidade certa
    habilidade_principal = models.CharField(max_length=20, choices=HABILIDADES_CHOICES, default='GERAL')
    disponibilidade = models.CharField(max_length=20, choices=DISPONIBILIDADE_CHOICES, default='VARIAVEL',help_text="Período principal de disponibilidade")

    # Local que irá atuar
    regiao_afetada_atuacao = models.ForeignKey(RegiaoAfetada, on_delete=models.SET_NULL, null=True, blank=True, related_name='regiao_atuacao', verbose_name="Região Destino")

    def __str__(self):
        return f"{self.nome_completo} ({self.get_habilidade_principal_display()})"

class Doacao(models.Model):
    """
    Representa o recurso doado.
    Foco: Rastreabilidade (Quantidade, Onde está / Para onde foi).
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    TIPO_ITEM = [
        ('AGUA', 'Água Potável'),
        ('ALIMENTO', 'Alimento Não Perecível'),
        ('ROUPA', 'Vestuário/Cama/Banho'),
        ('HIGIENE', 'Itens de Higiene'),
        ('MEDICAMENTO', 'Medicamentos'),
        ('DINHEIRO', 'Aporte Financeiro'),
        ('MATERIAL', 'Material para reforma'),
        ('OUTRO', 'Outros'),
    ]

    SITUACAO_CHOICES = [
        ('DISPONIVEL', 'Disponível / Em Estoque'),
        ('RESERVADO', 'Reservado para Região'),
        ('EM_TRANSITO', 'Em Trânsito / Saiu para Entrega'),
        ('ENTREGUE', 'Entregue ao Destino'),
    ]

    UNIDADE_CHOICES = [
        ('KG', 'Quilogramas (Kg)'),
        ('L', 'Litros (L)'),
        ('UN', 'Unidades (Un)'),
        ('CX', 'Caixas (Cx)'),
        ('PCT', 'Pacotes (Pct)'),
        ('FARDO', 'Fardos'),
        ('PALLET', 'Pallets'),
        ('OUTRO', 'Outro'),
    ]

    # Atributos das doações
    produto = models.CharField(max_length=100, help_text="Ex: Garrafas de 1.5L, Arroz 5kg")
    tipo = models.CharField(max_length=20, choices=TIPO_ITEM, default='OUTRO')
    quantidade = models.IntegerField(default=0)
    unidade_medida = models.CharField(max_length=20, blank=True, null=True, help_text="Ex: Litros, Kg, Unidades, Caixas")
    quantidade_por_volume = models.PositiveIntegerField(default=0)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='DISPONIVEL')
    
    # Para onde vai? (Fundamental para o gerenciamento)
    destino = models.ForeignKey(RegiaoAfetada, on_delete=models.SET_NULL, null=True, blank=True, related_name='recurso_enviado', verbose_name="Região Destino")
    
    data_doacao = models.DateTimeField(auto_now_add=True)
    entregue = models.BooleanField(default=False, verbose_name="Foi entregue ao destino?")

    def __str__(self):
        origem = self.voluntario.nome_completo if self.voluntario else 'Anônimo'
        destino_nome = self.destino.nome_identificacao if self.destino else 'Estoque Geral'
        return f"{self.quantidade}x {self.produto} ({origem} -> {destino_nome})"


