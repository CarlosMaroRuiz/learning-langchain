from langchain.tools import tool
import requests
import json
#procedemos crear nuestras tools para importar

#la tool se hace por medio de decoradores
#es necesario comentar para que el modelo sepa que es una herramienta y pueda usarla
@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Obtiene el clima actual dado latitud y longitud usando Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return json.dumps(data, indent=4)