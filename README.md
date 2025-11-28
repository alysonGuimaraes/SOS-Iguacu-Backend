# SOS Iguaçu - Backend (API)

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)
![Badge Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Badge Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Badge Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Repositório do projeto de avaliação A3 da UC de Gestão e Qualidade de Software. Este repositório contém o código fonte do backend (API) do projeto.

---

## 📝 Sobre o Projeto

O **SOS Iguaçu** é o módulo Backend da Plataforma Web desenvolvida para auxiliar a cidade de Rio Bonito do Iguaçu na reconstrução pós-tornado. 

Este módulo é responsável pela lógica de negócios, gestão do banco de dados e integrações externas. O sistema processa dados para geolocalização e priorização de danos, servindo como núcleo de inteligência para o front-end.

---

## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

* **Linguagem:** Python 3.x
* **Framework:** Django & Django REST Framework
* **Banco de Dados:** PostgreSQL (Hospedado na AWS)
* **Integrações / APIs Externas:**
    * **Nominatim (OpenStreetMap):** Utilizado para serviços de Geocodificação Reversa.
    * **ViaCEP:** Utilizado para consulta e validação de endereços postais.

---

## 📂 Estrutura do Projeto

A estrutura de diretórios do projeto está organizada da seguinte forma:

```text
SOS-IGUACU-BACKEND/
│
├── SOS_Iguacu_Backend/   # Configurações globais do projeto (Settings, URLs principais)
│
├── app/                  # Aplicação principal (Core logic)
│   ├── migrations/       # Histórico de alterações do banco de dados
│   ├── services/         # Integrações externas (Nominatim/ViaCEP)
│   ├── models.py         # Modelos do Banco de Dados (ORM)
│   ├── serializers.py    # Transformação de dados para JSON (API)
│   ├── tests.py          # Testes unitários
│   ├── urls.py           # Rotas específicas da aplicação
│   └── views.py          # Controladores (Lógica de requisição/resposta)
│
├── .env                  # Variáveis de ambiente (NÃO COMITADO)
├── .env.example          # Modelo das variáveis de ambiente
├── manage.py             # CLI do Django
└── requirements.txt      # Lista de dependências do projeto
```
-----

## Guia de Início Rápido (Setup Inicial)

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento pela primeira vez.

### Pré-requisitos

Certifique-se de que você tem o **Python 3.x**, o **Git** instalados em sua máquina e acesso às credenciais do banco AWS.

### Passo 1: Clonar e Acessar o Repositório

Abra seu terminal e execute os comandos:

```bash
# 1. Clonar o repositório
git clone https://github.com/alysonGuimaraes/SOS-Iguacu-Backend.git

# 2. Navegar para o diretório do projeto
cd SOS-Iguacu-Backend
```

### Passo 2: Criar e Ativar o Ambiente Virtual (`venv`)

É **obrigatório** utilizar um ambiente virtual para isolar as dependências do projeto, garantindo que as versões de biblioteca de todos os membros sejam idênticas.

```bash
# 3. Criar o ambiente virtual (venv)
python -m venv venv

# 4. Ativar o ambiente:
# Em sistemas Linux/macOS
source venv/bin/activate

# Em sistemas Windows (PowerShell)
.\venv\Scripts\Activate
```

### Passo 3: Variáveis de Ambiente (.env)
O projeto utiliza variáveis de ambiente para proteger dados sensíveis. Antes de avançar execute os seguintes passos:

1. Crie um arquivo chamado .env na raiz do projeto (mesmo nível do manage.py).

2. Copie o conteúdo de .env.example ou use o modelo abaixo preenchendo com as credenciais de acesso do banco de dados:

```Ini, TOML
# Exemplo de configuração do arquivo .env
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=host_da_aws_ou_localhost
DB_PORT=5432
SECRET_KEY=sua_chave_secreta_django
DEBUG=True
```

### Passo 4: Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no `requirements.txt`.

```bash
# 5. Instalar todas as dependências (incluindo Django)
pip install -r requirements.txt
```

### Passo 5: Migrações do Banco de Dados
Como estamos usando PostgreSQL, é necessário aplicar as migrações para criar as tabelas antes de rodar o projeto.

```Bash
python manage.py migrate
```

### Passo 6: Iniciar o Servidor de Desenvolvimento

Após a instalação das dependências, o servidor de desenvolvimento do Django pode ser iniciado.

```bash
# 6. Iniciar o servidor
python manage.py runserver
```

O Backend estará acessível em: **`http://127.0.0.1:8000/`**

-----

## Rodando os Testes
Para garantir a qualidade do código, o projeto possui testes unitários (localizados em app/tests.py). Para executá-los:

```Bash
# Rodar todos os testes
python manage.py test

# Rodar testes com mais detalhes (verbosity)
python manage.py test -v 2
```

-----

## Colaboração (Controle de Versão)

* **Branches:** Utilize *branches* para o desenvolvimento de novas funcionalidades (`feature/nome-da-feature`).
* **Commits:** Garanta que seus *commits* sejam atômicos e tenham mensagens claras.
* **Pull Requests:** Abra PRs para a branch main ou develop (conforme fluxo definido) para revisão de código.
