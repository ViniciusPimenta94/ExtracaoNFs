# Extração de Notas Fiscais com ChatGPT e Integração TWM

Este projeto automatiza a extração de dados de notas fiscais em PDF utilizando OCR e NLP com OpenAI (ChatGPT), e envia as informações extraídas para o sistema TWM.

---

## 📦 Estrutura do Projeto

- `baixar_pdf.py`: Realiza o download dos PDFs das faturas.
- `extrair_texto_pdf.py`: Aplica OCR ou leitura direta para extrair texto de PDFs.
- `chatgpt.py`, `openAI_management.py`, `respostas_chatgpt.py`: Lógica de chamada à API da OpenAI e interpretação semântica do conteúdo das NFs.
- `enviar_nota_twm.py`: Faz a integração dos dados extraídos com o sistema TWM.
- `conexao_twm.py`: Gerencia conexões com o backend TWM.
- `faturas_para_extrair_nf.py`: Organiza e gerencia o lote de faturas para processamento.
- `DAG_extracao_nf_gpt.py`: DAG de orquestração (possivelmente Airflow).

---

## ▶️ Como Executar

1. Configure o arquivo `configs/extracao_nf_gpt/appsettings.json` com as credenciais e parâmetros da API OpenAI e do sistema TWM.
2. Instale os requisitos:

```bash
pip install -r requirements.txt
```

3. Execute a sequência principal:

```bash
python faturas_para_extrair_nf.py
```

Ou para tarefas específicas:

```bash
python baixar_pdf.py
python extrair_texto_pdf.py
python enviar_nota_twm.py
```

---

## 🧠 Funcionalidades

- Interpretação automática de conteúdo de PDFs usando IA (GPT).
- Suporte a múltiplos clientes e múltiplos layouts de nota fiscal.
- Geração de logs, extrações estruturadas e falhas registradas.
- Integração com o sistema corporativo TWM.

---

## 📄 Licença

MIT
