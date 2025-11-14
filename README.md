# SOS Iguaçu - Backend (API)
Repositório do projeto de avaliação A3 da UC de Gestão e Qualidade de Software. Este repositório conterá o código fonte do backend do projeto.

-----

# Ideia do projeto

O **SOS Iguaçu** é o módulo Backend (API) da Plataforma Web desenvolvida para auxiliar a cidade de Rio Bonito do Iguaçu na reconstrução pós-tornado. Este módulo é responsável pela lógica de negócios, gestão do banco de dados e integração com APIs externas (Nominatim/OpenStreetMap) para geolocalização e priorização de danos.

-----

## Tecnologias Utilizadas

  * **Linguagem:** Python 3.x
  * **Framework:** Django
  * **Banco de Dados:** SQLite (Desenvolvimento Inicial)
  * **Integração API:** Nominatim (Geocodificação Reversa)

-----

## Guia de Início Rápido (Setup Inicial)

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento pela primeira vez.

### Pré-requisitos

Certifique-se de que você tem o **Python 3.x** e o **Git** instalados em sua máquina.

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

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no `requirements.txt`.

```bash
# 5. Instalar todas as dependências (incluindo Django)
pip install -r requirements.txt
```

### Passo 4: Iniciar o Servidor de Desenvolvimento

Após a instalação das dependências, o servidor de desenvolvimento do Django pode ser iniciado.

```bash
# 6. Iniciar o servidor
python manage.py runserver
```

O Backend estará acessível em: **`http://127.0.0.1:8000/`**

-----

## Colaboração (Controle de Versão)

  * **Branches:** Utilize *branches* para o desenvolvimento de novas funcionalidades (`feature/nome-da-feature`).
  * **Commits:** Garanta que seus *commits* sejam atômicos e tenham mensagens claras.
