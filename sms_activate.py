import requests
from config import API_KEY_SMSACTIVATE

class SMSActivateClient:
    def __init__(self):
        self.api_key = API_KEY_SMSACTIVATE
        self.base_url = "https://api.sms-activate.org/stubs/handler_api.php"

    def obtener_numero(self, servicio, pais=0):
        params = {
            "api_key": self.api_key,
            "action": "getNumber",
            "service": servicio,
            "country": pais
        }
        response = requests.get(self.base_url, params=params).text
        if "ACCESS_NUMBER" in response:
            parts = response.split(":")
            return parts[2], parts[1]  # número, activation_id
        else:
            return None

    def obtener_codigo(self, activation_id):
        params = {
            "api_key": self.api_key,
            "action": "getStatus",
            "id": activation_id
        }
        response = requests.get(self.base_url, params=params).text
        if "STATUS_OK" in response:
            return response.replace("STATUS_OK:", "")
        elif response == "STATUS_WAIT_CODE":
            return "⏳ Aún no ha llegado el código. Intenta más tarde."
        else:
            return response

    def cancelar_activacion(self, activation_id):
        params = {
            "api_key": self.api_key,
            "action": "setStatus",
            "status": 8,
            "id": activation_id
        }
        requests.get(self.base_url, params=params)