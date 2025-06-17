import time
import json
from openai import OpenAI
from extrair_texto_pdf import extrair_texto_pdf
from openAI_management import getConteudoConfigByName

# Carregar configurações
config = getConteudoConfigByName('appsettings')
client = OpenAI(api_key=config['ChatGPT']['OpenApiKey'])

def perguntar_sobre_pdf(caminho_pdf, fornecedor, id_thread_gpt, id_assistant_gtp, id_fatura_base):
    try:
        # 1. Extrair texto do PDF
        texto_pdf = extrair_texto_pdf(caminho_pdf)
        if not texto_pdf:
            return None
        
        # 2. Limpar a thread antes de enviar uma nova mensagem
        mensagens_existentes = client.beta.threads.messages.list(thread_id=id_thread_gpt)
        for mensagem in mensagens_existentes.data:
            client.beta.threads.messages.delete(thread_id=id_thread_gpt, message_id=mensagem.id)

        # 3. Enviar mensagem com o texto
        client.beta.threads.messages.create(
            thread_id=id_thread_gpt,
            role="user",
            content=texto_pdf
        )

        # 4. Criar e monitorar run
        model = {
            "CABO TELECOM": "gpt-4o",
            "VALENET": "gpt-4o",
            "INTERNET SUPER": "gpt-4o",
        }.get(fornecedor, config['ChatGPT']['ModelName'])

        run = client.beta.threads.runs.create(
            thread_id=id_thread_gpt,
            assistant_id=id_assistant_gtp,
            model=model
        )

        # 5. Monitorar execução
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=id_thread_gpt,
                run_id=run.id
            )
            
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return None
            time.sleep(1)

        # 6. Obter resposta
        messages = client.beta.threads.messages.list(
            thread_id=id_thread_gpt,
            order="desc",
            run_id=run.id
        )

        if messages.data:
            resposta = messages.data[0].content[0].text.value
            try:
                # Limpar e parsear JSON
                json_str = resposta.replace('```json', '').replace('```', '').strip()
                resultado = json.loads(json_str)
                
                return resultado
            except json.JSONDecodeError:
                return None

        return None

    except Exception as e:
        return None
