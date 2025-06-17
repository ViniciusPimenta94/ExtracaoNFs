import json
import requests
from os.path import join
from conexao_twm import obter_token
from dto_structure import NOTA_FISCAL_DTO

import os
import json
from os.path import join

def getConteudoConfigByName(nm_json_config) -> dict:
    caminho_env = os.environ.get("CONFIG_FILE")

    if caminho_env and os.path.isfile(caminho_env):
        caminho_arquivo = caminho_env
    else:
        caminho_arquivo = join(
            r'D:\ExtracaoNF\configs',
            'extracao_nf_gpt',
            f'{nm_json_config}.json'
        )

    with open(caminho_arquivo, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data
def verificar_instructions_assistant(client, id_assistant_gtp, prompt_extracao_nf):
    """Verifica se as instruções do Assistant estão atualizadas"""
    try:
        prompt_chatgpt = (
            f"Você é um assistente especializado em analisar documentos PDF e extrair informações estruturadas. "
            f"Analise o documento e extraia as informações que correspondam à estrutura do DTO fornecido. "
            f"Responda APENAS com um objeto JSON que corresponda exatamente à estrutura do DTO fornecido. "
            f"Não inclua explicações ou texto adicional, apenas o JSON.\n\n"
            f"Estrutura do DTO para extração:\n"
            f"{NOTA_FISCAL_DTO}\n\n"
            f"REGRAS ESSENCIAIS:\n"
            f"{prompt_extracao_nf}\n"
        )

        assistant = client.beta.assistants.retrieve(id_assistant_gtp)
                
        # Verificar se as instruções do Assistant precisam ser atualizadas
        if normalizar_prompt(assistant.instructions) != normalizar_prompt(prompt_chatgpt):
            try:
                updated_assistant = client.beta.assistants.update(
                    assistant_id=assistant.id,
                    instructions=prompt_chatgpt
                )
                id_assistant_gtp = updated_assistant.id  # Atualiza o ID caso tenha mudado
            except Exception as e:
                return None

        return id_assistant_gtp
    except Exception as e:
        return None

def obter_thread_id(client, config, fornecedor, id_thread_gpt, id_assistant_gtp, prompt_extracao_nf):
    try:
        novo_assistant = False
        novo_thread = False

        if id_assistant_gtp and id_thread_gpt:
            try:
                assistant = client.beta.assistants.retrieve(id_assistant_gtp)
            except Exception:
                return None
            try:
                thread = client.beta.threads.retrieve(id_thread_gpt)
            except Exception:
                return None

        else:
            assistant = criar_assistant(client, config, fornecedor, prompt_extracao_nf)
            thread = criar_thread(client)
            novo_assistant = True
            novo_thread = True

        if novo_assistant or novo_thread:
            atualizar_fornecedor_twm(config, fornecedor, thread.id, assistant.id)

        return thread.id, assistant.id if assistant else None

    except Exception as e:
        return None, None

def normalizar_prompt(prompt):
    """Normaliza o prompt para comparação removendo espaços extras e normalizando quebras de linha"""
    import re
    # Remove múltiplos espaços, tabs e normaliza quebras de linha
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    return prompt
    
def criar_assistant(client, config, fornecedor, prompt_extracao_nf):
    try:
        prompt_chatgpt = (
            f"Você é um assistente especializado em analisar documentos PDF e extrair informações estruturadas. "
            f"Analise o documento e extraia as informações que correspondam à estrutura do DTO fornecido. "
            f"Responda APENAS com um objeto JSON que corresponda exatamente à estrutura do DTO fornecido. "
            f"Não inclua explicações ou texto adicional, apenas o JSON.\n\n"
            f"Estrutura do DTO para extração:\n"
            f"{NOTA_FISCAL_DTO}\n\n"
            f"REGRAS ESSENCIAIS:\n"
            f"{prompt_extracao_nf}\n"
        )

        assistant = client.beta.assistants.create(
            name=f"FOR {fornecedor}",
            instructions=prompt_chatgpt,
            model=config['ChatGPT']['ModelName'],
            tools=[
                {"type": "file_search"},
                {"type": "code_interpreter"}
            ],
            temperature=0.25
        )
        return assistant
    except Exception as e:
        return None

def criar_thread(client):
    try:
        thread = client.beta.threads.create()
        return thread
    except Exception as e:
        return None
