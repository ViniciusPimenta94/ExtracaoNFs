import json
import os
import requests
import shutil
from baixar_pdf import baixar_pdf_ged
from conexao_twm import obter_token
from processar_pdf import processar_pdf 
from openAI_management import obter_thread_id, getConteudoConfigByName, verificar_instructions_assistant
from openai import OpenAI

def criar_diretorio_respostas():
    """Cria o diretório de respostas se não existir"""
    if not os.path.exists('respostas'):
        os.makedirs('respostas')

def salvar_resposta_faturas(dados, fornecedor):
    """Salva a resposta das faturas em arquivo JSON"""
    nome_arquivo = f"respostas/faturas_sem_nf_{fornecedor}.json"
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        return False

def obter_faturas_para_extrair_nf(fornecedor, config):
    """Obtém faturas para extrair nota fiscal do TWM"""
    try:
        token = obter_token()
        if not token:
            return None
        
        data_inicio = config['dataInicio']
        url_twm = f"https://{config['subdominio']}.telecomwm.com.br"
        endpoint = config['TWM']['FaturasParaExtrairNotaFiscalEndpoint']
        url_faturas = f"{url_twm}/{endpoint}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        params = {
            'fornecedor': fornecedor,
            'dataInicio': data_inicio
        }

        response = requests.get(url_faturas, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None
    
def processar_faturas(faturas, fornecedor):
    """Processa cada fatura, baixando PDF e extraindo informações"""
    if not isinstance(faturas, list):
        return False

    config = getConteudoConfigByName('appsettings')
    client = OpenAI(api_key=config['ChatGPT']['OpenApiKey'])

    for fatura in faturas:
        if not all(key in fatura for key in ['dcUrlGed', 'idFaturaBase', 'dcPromptExtracaoNF']):
            continue

        id_thread_gpt = fatura.get('idThreadGPT')
        id_assistant_gpt = fatura.get('idAssistantGPT')

        if id_assistant_gpt:
            verificar_instructions_assistant(
                client, id_assistant_gpt, fatura['dcPromptExtracaoNF']
            )

        # Verifica se os IDs existem, se não, cria novos
        if not id_thread_gpt or not id_assistant_gpt:
            id_thread_gpt, id_assistant_gpt = obter_thread_id(
                client, config, fornecedor, id_thread_gpt, id_assistant_gpt, fatura['dcPromptExtracaoNF']
            )
            if not id_thread_gpt or not id_assistant_gpt:
                continue
            break

        arquivo_pdf = baixar_pdf_ged(
            fatura['dcUrlGed'], 
            fatura['idFaturaBase'], 
            fornecedor
        )

        if arquivo_pdf:
            processar_pdf(
                caminho_pdf=arquivo_pdf,
                fornecedor=fornecedor,
                id_fatura_base=fatura['idFaturaBase'],
                id_thread_gpt=id_thread_gpt,
                id_assistant_gtp=id_assistant_gpt
            )

            pasta_pdf = os.path.dirname(arquivo_pdf)
            try:
                shutil.rmtree(pasta_pdf)
            except Exception as e:
                continue

    return True

def main():
    config_name = os.path.splitext(os.path.basename(os.environ.get("CONFIG_FILE", "appsettings.json")))[0]
    config = getConteudoConfigByName(config_name)
    
    if not config:
        return
    
    fornecedores = config['fornecedor'] if isinstance(config['fornecedor'], list) else [config['fornecedor']]

    for fornecedor in fornecedores:
        print(f"Processando faturas para o fornecedor: {fornecedor}")
        
        faturas = obter_faturas_para_extrair_nf(fornecedor, config)
        if not faturas:
            continue

        if not processar_faturas(faturas, fornecedor):
            break

def extrair_faturas_nf():
    main()

if __name__ == "__main__":
    extrair_faturas_nf()
