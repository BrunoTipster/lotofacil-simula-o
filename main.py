import requests
from bs4 import BeautifulSoup
import json

# URL da página da Lotofácil
url = "https://www.megasena.com/lotofacil/resultados"

def fetch_results(url):
    # Fazendo a solicitação HTTP para obter o conteúdo da página
    response = requests.get(url)
    html_content = response.content

    # Analisando o HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrando o último resultado
    last_result = soup.find('table', class_='_results _archive -center facil')
    draw_number = last_result.find('div', class_='draw-number').strong.text
    draw_date = last_result.find('div', class_='date').text.strip()

    # Extraindo os números sorteados
    numbers = []
    balls = last_result.find_all('li', class_='ball facil')
    for ball in balls:
        numbers.append(ball.text)

    # Armazenando o último resultado
    results = [{
        "concurso": draw_number,
        "data": draw_date,
        "numeros": numbers
    }]

    # Encontrando resultados anteriores
    previous_results = soup.find_all('tr')[2:]  # Ignorando os cabeçalhos

    for result in previous_results:
        draw_info = result.find('div', class_='draw-number')
        if draw_info:
            draw_number = draw_info.strong.text
            draw_date = result.find('div', class_='date').text.strip()
            numbers = [ball.text for ball in result.find_all('li', class_='ball facil')]
            results.append({
                "concurso": draw_number,
                "data": draw_date,
                "numeros": numbers
            })

    return results

def save_results_to_json(results, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

# Executa as funções
results = fetch_results(url)
save_results_to_json(results, 'lotofacil_results.json')
