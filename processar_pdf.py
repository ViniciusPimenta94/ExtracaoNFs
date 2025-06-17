import os
from respostas_chatgpt import verificar_campos_nulos
from chatgpt import perguntar_sobre_pdf
from enviar_nota_twm import enviar_nota_fiscal

def processar_pdf(caminho_pdf, fornecedor, id_fatura_base, id_thread_gpt, id_assistant_gtp):
    """Processa um PDF para extração de dados de notas fiscais usando OpenAI"""
    if not os.path.exists(caminho_pdf):
        return

    resposta = perguntar_sobre_pdf(
        caminho_pdf=caminho_pdf,
        fornecedor=fornecedor,
        id_thread_gpt=id_thread_gpt,
        id_assistant_gtp=id_assistant_gtp,
        id_fatura_base=id_fatura_base
    )

    if not resposta:
        return

    # Garante que é uma lista de notas
    notas = resposta if isinstance(resposta, list) else [resposta]
    notas_processadas = 0

    for idx, nota in enumerate(notas, start=1):

        if verificar_campos_nulos(nota):
            continue

        # if salvar_resposta_json(nota, id_fatura_base, fornecedor):
        if enviar_nota_fiscal(nota, id_fatura_base):
            notas_processadas += 1
            