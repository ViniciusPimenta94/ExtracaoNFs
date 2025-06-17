import pdfplumber
import fitz  # PyMuPDF
import warnings

# Ignore specific pdfplumber warnings about CropBox
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")

def extrair_com_pdfplumber(caminho_pdf):
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = ""
            for i, page in enumerate(pdf.pages):
                try:
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        texto += texto_pagina + "\n"
                except Exception as e:
                    continue
        if texto.strip():
            return texto.strip()
        else:
            return None
    except Exception as e:
        return None

def extrair_com_pymupdf(caminho_pdf):
    try:
        texto = ""
        with fitz.open(caminho_pdf) as doc:
            for i, page in enumerate(doc):
                texto_pagina = page.get_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"
        if texto.strip():
            return texto.strip()
        else:
            return None
    except Exception as e:
        return None

def extrair_texto_pdf(caminho_pdf):
    texto = extrair_com_pymupdf(caminho_pdf)
    if not texto:
        texto = extrair_com_pdfplumber(caminho_pdf)
    return texto
