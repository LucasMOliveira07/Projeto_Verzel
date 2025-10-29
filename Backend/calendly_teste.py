import os
import requests
from dotenv import load_dotenv

load_dotenv()
chave_API_CALENDLY = os.getenv("chave_API_CALENDLY")

if not chave_API_CALENDLY:
    raise ValueError("A chave da API do Calendly não foi encontrada no arquivo Backend/.env.")

headers = {
    "Authorization": f"Bearer {chave_API_CALENDLY}",
    "Content-Type": "application/json"
}

user_response = requests.get("https://api.calendly.com/users/me", headers=headers)
if user_response.status_code != 200:
    print(f"Erro: {user_response.status_code} - {user_response.text}")
    raise ValueError("Não foi possível obter informações do usuário do Calendly.")

try:
    user_data = user_response.json()
    user_uri = user_data['resource']['uri']
    print(f"Usuário encontrado: {user_data['resource']['name']}")
except Exception as e:
    print(f"Erro ao processar a resposta do Calendly: {e}")
    print(f"Resposta recebida: {user_response.text}")

print("A buscar 'Tipos de Evento' (os seus modelos de reunião)...")

events_response = requests.get(
    "https://api.calendly.com/event_types",
    headers=headers,
    params={"user": user_uri})

if events_response.status_code != 200:
    print(f"Erro: {events_response.status_code} - {events_response.text}")
    raise ValueError("Não foi possível obter os TIPOS DE EVENTO do Calendly.")

events_data = events_response.json()
events_types = events_data.get("collection", [])

print("Eventos do Calendly obtidos com sucesso:")
found = False
for event in events_types:
    if event.get("active"):
        print(f"Evento: {event['name']}")
        print(f"URI: {event['uri']}")
        found = True

if not found:
    print("Nenhum evento ativo encontrado.")
else:
    print("Eventos listados.")
