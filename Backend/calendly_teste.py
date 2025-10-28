import os
import requests
from dotenv import load_dotenv

load_dotenv()
chave_API_CALENDLY = os.getenv("chave_API_CALENDLY")

if not chave_API_CALENDLY:
    raise ValueError("A chave da API do Calendly não foi encontrada no arquivo Backend/.env.")
exit()

headers = { 
    "Authorization": f"Bearer {chave_API_CALENDLY}",
    "Content-Type": "application/json"
}
user_response = requests.get("https://api.calendly.com/users/me", headers=headers)
if user_response.status_code != 200:
    raise ValueError("Não foi possível obter informações do usuário do Calendly.")
    print(f"Erro: {user_response.status_code} - {user_response.text}")
    print("Verifique se a chave da API está correta.")
    exit()

try:
    user_data = user_response.json()
    user_uri = user_data['resource']['uri']
    print(f"Usuário encontrado: {user_data['resource']['name']}")
except Exception as e:
    raise ValueError("Erro ao processar a resposta do Calendly.")
    print(f"Resposta recebida: {user_response.text}")
    exit()

events_response = requests.get(f"https://api.calendly.com/scheduled_events?user={user_uri}", headers=headers)
if events_response.status_code != 200:
    raise ValueError("Não foi possível obter eventos agendados do Calendly.")
    print(f"Erro: {events_response.status_code} - {events_response.text}")
    exit()

print("Eventos do Calendly obtidos com sucesso:")
found = False
for event in events_types:
    if event["active"]:
        print(f"Evento: {event['name']}")
        print(f"URI: {event['uri']}")
if not found:
    print("Nenhum evento ativo encontrado.")
else:
    print("Eventos listados:")