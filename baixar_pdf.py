import requests
import os
from openAI_management import getConteudoConfigByName

def baixar_pdf_ged(dc_url_ged, id_fatura_base, fornecedor):
    try:
        # Carregar configurações
        config = getConteudoConfigByName('appsettings')

        # Preparar a URL e headers
        url = config['Annie']['UrlBaixarPdf']
        headers = {
            'Content-Type': 'application/json',
            'ApiKeyGed': config['Annie']['ApiKeyGed']
        }

        # Preparar o body da requisição
        body = {
            "urlDownload": dc_url_ged
        }

        # Fazer a requisição POST
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        # Criar diretório para PDFs se não existir
        if not os.path.exists('pdfs'):
            os.makedirs('pdfs')

        # Criar diretório específico para o fornecedor
        pasta_fornecedor = os.path.join('pdfs', fornecedor)
        if not os.path.exists(pasta_fornecedor):
            os.makedirs(pasta_fornecedor)

        # Gerar nome do arquivo com idFaturaBase
        nome_arquivo = os.path.join(pasta_fornecedor, f"{id_fatura_base}.pdf")

        # Salvar o PDF
        with open(nome_arquivo, 'wb') as f:
            f.write(response.content)

        return nome_arquivo

    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None 