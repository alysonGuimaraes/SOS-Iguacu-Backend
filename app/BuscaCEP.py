from django import request

def buscar_endereco_por_cep(cep):
    """
    Busca o endereço completo usando a API gratuita ViaCEP.
    Retorna um dicionário com os dados de endereço ou None em caso de erro.
    """
    # Remove qualquer caractere não numérico do CEP (hífen, ponto, etc.)
    cep_limpo = ''.join(filter(str.isdigit, str(cep)))
    
    if len(cep_limpo) != 8:
        return None 
        
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        data = response.json()

        if data.get('erro'):
            return None 

        return {
            'endereco': data.get('logradouro'),
            'bairro': data.get('bairro'),
            'cidade': data.get('localidade'),
            'uf': data.get('uf'),
            'cep_formatado': data.get('cep'),
        }
    
    except requests.RequestException as e:
        print(f"Erro ao consultar ViaCEP: {e}")
        return None
