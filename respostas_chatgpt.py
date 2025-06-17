import os
import json
from datetime import datetime
from openAI_management import getConteudoConfigByName

# Carregar configurações
config = getConteudoConfigByName('appsettings')

def salvar_resposta_json(resposta, nome_arquivo, fornecedor):
    try:
        pasta_fornecedor = os.path.join(config['ChatGPT']['RESPOSTAS_DIR'], fornecedor)
        os.makedirs(pasta_fornecedor, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo_completo = os.path.join(pasta_fornecedor, f"{nome_arquivo}_{timestamp}.json")
        
        with open(nome_arquivo_completo, 'w', encoding='utf-8') as f:
            json.dump(resposta, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        return False

def verificar_campos_nulos(objeto):
    if not isinstance(objeto, dict):
        return objeto is None or objeto == ""

    if 'Numero' in objeto and (objeto['Numero'] is None or objeto['Numero'] == ""):
        return True
    
    if 'ItensNotaFiscal' in objeto:
        itens = objeto['ItensNotaFiscal']
        if not itens or not isinstance(itens, list):
            return True

    return all(verificar_campos_nulos(valor) for valor in objeto.values())
