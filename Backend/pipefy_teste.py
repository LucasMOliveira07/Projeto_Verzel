import os
import requests
from dotenv import load_dotenv

load_dotenv()
chave_API_PIPEFY = os.getenv("chave_API_PIPEFY")
if not chave_API_PIPEFY:
    raise ValueError("A chave_API_PIPEFY não foi encontrada no arquivo .env.")
else:
    print("Chave API carregada com sucesso.")

API_URL = "https://api.pipefy.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {chave_API_PIPEFY}",
    "Content-Type": "application/json"
}

# --- Parte 1: Encontrar o Funil ---
query_pipes = {
    "query": """
    {
      organizations {
        id
        name
        pipes {
          id
          name
        }
      }
    }
    """
}

print("Procurando o id do seu funil de pré-vendas...")
pipe_id = None
try:
    response = requests.post(API_URL, json=query_pipes, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        print("Erro na resposta da API (Parte 1):", data["errors"])
        exit()
        
    organizations = data["data"].get("organizations", [])
    if not organizations:
        print("Erro: Nenhuma organização encontrada.")
        exit()

    all_pipes = []
    for org in organizations:
        all_pipes.extend(org.get("pipes", [])) 

    if not all_pipes:
        print("Erro: Nenhum funil encontrado nas suas organizações.")
        exit()
        
    for pipe in all_pipes:
        pipe_name_lower = pipe["name"].lower()
        if pipe_name_lower == "pré-vendas" or pipe_name_lower == "pre-vendas":
            pipe_id = pipe["id"]
            break
            
    if not pipe_id:
        print("Funil 'pre-vendas' ou 'pré-vendas' não encontrado.")
        exit()
        
    print(f"Funil 'pre-vendas' encontrado com ID: {pipe_id}")

except requests.exceptions.RequestException as e:
    print("Erro ao conectar à API do Pipefy (Parte 1):", e)
    exit()


# --- Parte 2: Encontrar os Campos ---
# (Usando o pipe_id da Parte 1)
query_acha_campos = {
    "query": f"""
    query {{
      pipe(id: "{pipe_id}") {{
        start_form_fields {{
          id
          label
        }}
      }}
    }}
    """
}

print(f"Buscando os campos do funil com ID: {pipe_id}...")
try:
    response = requests.post(API_URL, json=query_acha_campos, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        print("Erro na resposta da API (Parte 2):", data["errors"])
        exit()

    fields = data["data"]["pipe"]["start_form_fields"]
    print("Campos encontrados no formulário inicial:")

    if not fields:
        print("Nenhum campo encontrado.")
        exit()

    for field in fields:
        print(f"Nome do Campo: '{field['label']}'  ==>  ID do Campo: '{field['id']}'")

except requests.exceptions.RequestException as e:
    print("Erro ao conectar à API do Pipefy (Parte 2):", e)
    exit()