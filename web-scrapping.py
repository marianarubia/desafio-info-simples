import requests
from bs4 import BeautifulSoup
import json

url = 'https://infosimples.com/vagas/desafio/commercia/product.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

resposta_final = {
    'title': soup.select_one('h2#product_title').get_text() if soup.select_one('h2#product_title') else "Título não encontrado",
    'price': soup.select_one('.prod-pnow').get_text() if soup.select_one('.prod-pnow') else "Preço não encontrado",
    'description': soup.select_one('.proddet p').get_text(strip=True) if soup.select_one('.proddet p') else "Descrição não encontrada",
    'especificacoes': {row.find_all(['td', 'th'])[0].get_text(strip=True): row.find_all(['td', 'th'])[1].get_text(strip=True)
                       for row in soup.find_all('tr') if len(row.find_all(['td', 'th'])) == 2},
    'additional_properties': {
        row.find_all('td')[0].get_text(strip=True): row.find_all('td')[1].get_text(strip=True)
        for row in (soup.find('h4', string='Additional properties') or {}).find_next('table', {}).find_all('tr')
        if len(row.find_all('td')) == 2
    },
    'reviews': [{'comment': review.find('p').get_text(strip=True) if review.find('p') else ''}
                for review in soup.find_all('div', class_='analisebox')],
    'average_score': (soup.find('div', id='comments') or {}).find('h4').get_text(strip=True) if soup.find('div', id='comments') else ""
}

with open('produto.json', 'w') as arquivo_json:
    json.dump(resposta_final, arquivo_json, indent=4, ensure_ascii=False)
