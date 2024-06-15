import requests
from bs4 import BeautifulSoup

def extract_links():
    url = "https://ru.unb.br/index.php/cardapio-refeitorio"
    base_url = "https://ru.unb.br"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    darcy_section = soup.find(string="Darcy Ribeiro")

    links = []

    if darcy_section:
        for sibling in darcy_section.find_all_next(string=True):
            if sibling.parent.name == 'a' and sibling.parent['href'].endswith(".pdf"):
                
                if "darcy" in sibling.parent['href'].lower():
                    absolute_url = base_url + sibling.parent['href']
                    links.append(absolute_url)

    return links

#print(extract_links())