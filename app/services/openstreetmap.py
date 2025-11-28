import requests
from django.core.cache import cache

class OpenStreetMapClient:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/reverse"
        self.timeout = 10
        self.headers = {
            'User-Agent': 'SOS-iguacu/1.0'
        }
        self.cache_ttl = 86400 # 1 dia

    def buscar_endereco(self, latitude, longitude):
        """
        Converte Lat/Lon em endereço legível.
        """
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'zoom': 18,        # Nível de precisão (18 = número da casa)
            'addressdetails': 1
        }

        # Define uma chave unica para cada CEP 
        cache_key = f"nominatim_{latitude}_{longitude}"
        
        # Tenta utilizar a chave para buscar do cache
        dados_cache = cache.get(cache_key)

        if dados_cache:
            # print("Buscando endereço... Cache")
            return {"success": True, "data": dados_cache}

        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()

            # Caso a API da OpenStreet map não encontre nada ela retorna uma chave "error" no corpo da resposta
            if "error" in data:
                return {"success": False, "error": "Não foi possível realizar a geolocalização reversa"}
            
            if data.get('address') == {}:
                return {"success": False, "error": "Não foi possível encontrar informações de endereço para as coordenadas inseridas"}

            # Limpando a resposta (DTO simples)
            endereco_formatado = {
                "rua": data.get('address', {}).get('road', ''),
                "numero": data.get('address', {}).get('house_number', 'S/N'),
                "bairro": data.get('address', {}).get('city_district', '') or data.get('address', {}).get('suburb', ''),
                "cidade": data.get('address', {}).get('town', '') or data.get('address', {}).get('city', ''),
                "estado": data.get('address', {}).get('state', ''),
                "cep": data.get('address', {}).get('postcode', '')
            }

            # print("Buscando endereço... API openstreetmap")
            cache.set(cache_key, endereco_formatado, self.cache_ttl)

            return {"success": True, "data": endereco_formatado}

        except requests.RequestException as e:
            return {"success": False, "error": f"Erro na geolocalização: {str(e)}"}