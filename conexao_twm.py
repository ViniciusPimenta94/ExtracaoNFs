import requests
from requests.exceptions import RequestException
from os.path import join
import json

def getConteudoConfigByName(nm_json_config) -> dict:
    caminho_arquivo = join(
        r'D:\\ExtracaoNF\\configs',
        'extracao_nf_gpt',
        f'{nm_json_config}.json'
    )
    with open(caminho_arquivo, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data

def obter_token():
    try:
        # Carregar as credenciais do arquivo JSON
        credenciais = getConteudoConfigByName('appsettings')

        # Montar a URL com o subdomínio
        url_twm = f"https://{credenciais['subdominio']}.telecomwm.com.br"
        url_obter_token = f"{url_twm}/{credenciais['TWM']['TokenEndpoint']}"

        # Preparar os headers e o body da requisição
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'password',
            'username': credenciais['username'],
            'password': credenciais['password']
        }

        # Fazer a requisição POST
        response = requests.post(url_obter_token, headers=headers, data=body)
        response.raise_for_status()
        
        return response.json()['access_token']
    except RequestException as e:
        return None
    except Exception as e:
        return None

if __name__ == "__main__":
    # Teste a função quando executar o arquivo diretamente
    token = obter_token()