from links import extract_links
import requests
import fitz
import pandas as pd

def download_pdf(pdf_url, filename):
    response = requests.get(pdf_url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def process_text(text):
    
    lines = text.split('\n')
    cardapio = [line.strip() for line in lines if line.strip() != '']
        
    with open("cardapio.txt", "w", encoding="utf-8") as text_file:
        for line in cardapio:
            text_file.write(line + "\n")
    
    sections = ["Café da manhã", "Almoço", "Jantar"]
    days = ["2ª FEIRA", "3ª FEIRA", "4ª FEIRA", "5ª FEIRA", "6ª FEIRA", "SÁBADO", "DOMINGO"]

    # Dicionário para armazenar dados
    data = {day: {section: [] for section in sections} for day in days}
    
    current_section = None
    current_day = None

    for line in cardapio:
        # Identificar seções
        if any(section in line for section in sections):
            current_section = line
            continue
        
        # Identificar dias
        if any(day in line for day in days):
            current_day = line
            continue
        
        # Adicionar itens ao dicionário de dados
        if current_section and current_day:
            data[current_day][current_section].append(line)

    # Converter dicionário em DataFrame
    dfs = {}
    for section in sections:
        df_data = {day: data[day][section] for day in days}
        dfs[section] = pd.DataFrame.from_dict(df_data, orient='index').transpose()

    return dfs

links = extract_links()

# Processar cada link
# Processar cada link
for i, pdf_url in enumerate(links):
    pdf_path = f"cardapio_{i}.pdf"
    download_pdf(pdf_url, pdf_path)
    text = extract_text_from_pdf(pdf_path)
    data = process_text(text)
    for section, df in data.items():
        print(f"Dados extraídos do {section} do PDF {i + 1}:")
        print(df)