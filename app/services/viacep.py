import requests
from django.core.cache import cache

class ViaCepClient:
    def __init__(self):
        self.base_url = "https://viacep.com.br/ws"
        self.timeout = 5 # Timeout caso a chamada para a API externa demore demais
        self.cache_ttl = 86400 # 1 dia

    def consultar_cep(self, cep):
        """
        Versão Síncrona usando requests.
        """
        clean_cep = str(cep).replace("-", "").replace(".", "")
        url = f"{self.base_url}/{clean_cep}/json/"

        # Define uma chave unica para cada CEP 
        cache_key = f"viacep_{clean_cep}"
        
        # Tenta utilizar a chave para buscar do cache
        dados_cache = cache.get(cache_key)

        if dados_cache:
            # print("Buscando viaCEP... Cache")
            return {"success": True, "data": dados_cache}

        try:
            response = requests.get(url, timeout=self.timeout)
            
            # Levanta erro se ter um status de erro
            response.raise_for_status()
            
            data = response.json()

            resposta = {
                'logradouro': data.get('logradouro'),
                'bairro': data.get('bairro'),
                'cidade': data.get('localidade'),
                'uf': data.get('uf'),
                'cep': str(data.get('cep')).replace("-", "").replace(".", ""),
            }

            # ViaCep retorna 200 mesmo se o CEP não existe, mas manda um json {'erro': true}
            if "erro" in data:
                return {"success": False, "error": "CEP não encontrado na base"}
            
            # print("Buscando CEP... API viacep")
            cache.set(cache_key, resposta, self.cache_ttl)

            return {"success": True, "data": resposta}

        except requests.exceptions.Timeout:
            return {"success": False, "error": "O serviço de CEP demorou muito para responder"}
            
        except requests.exceptions.RequestException as e:
            # Captura qualquer erro de rede ou HTTP
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}