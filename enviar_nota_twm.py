import requests
from conexao_twm import obter_token
from openAI_management import getConteudoConfigByName

def enviar_nota_fiscal(nota_fiscal, id_fatura_base):
    """Envia a nota fiscal para o TWM."""
    try:
        # Carregar as configurações do TWM
        config = getConteudoConfigByName('appsettings')
        
        # Obter o token de autenticação
        token = obter_token()
        if not token:
            print("Falha ao obter token de autenticação.")
            return False

        # Montar a URL com o subdomínio
        url_twm = f"https://{config['subdominio']}.telecomwm.com.br"
        url_endpoint = f"{url_twm}/{config['TWM']['NotaFiscalEndpoint']}"
        
        # Preparar os headers
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Preparar o corpo da requisição com o formato esperado
        payload = {
            'IdFatura': id_fatura_base,
            'NotaFiscal': nota_fiscal
        }

        # Fazer a requisição POST
        response = requests.post(url_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        print("Nota fiscal enviada com sucesso.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Falha ao enviar nota fiscal: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False 