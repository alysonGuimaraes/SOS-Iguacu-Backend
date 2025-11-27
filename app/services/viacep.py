import requests

class ViaCepClient:
    def __init__(self):
        self.base_url = "https://viacep.com.br/ws"
        # Timeout é CRUCIAL no requests, pois o padrão é infinito (pode travar seu app)
        self.timeout = 5 

    def consultar_cep(self, cep):
        """
        Versão Síncrona usando requests.
        """
        clean_cep = str(cep).replace("-", "").replace(".", "")
        url = f"{self.base_url}/{clean_cep}/json/"

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

            return {"success": True, "data": resposta}

        except requests.exceptions.Timeout:
            return {"success": False, "error": "O serviço de CEP demorou muito para responder"}
            
        except requests.exceptions.RequestException as e:
            # Captura qualquer erro de rede ou HTTP
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}