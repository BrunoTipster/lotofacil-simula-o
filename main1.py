import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from collections import Counter
import tkinter as tk
from tkinter import ttk

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

def get_most_common_numbers(results):
    all_numbers = []
    for result in results:
        all_numbers.extend(result['numeros'])
    counter = Counter(all_numbers)
    return counter.most_common()

def display_results(results):
    root = tk.Tk()
    root.title("Resultados da Lotofácil")

    columns = ('concurso', 'data', 'numeros')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('concurso', text='Concurso')
    tree.heading('data', text='Data')
    tree.heading('numeros', text='Números Sorteados')

    for result in results:
        tree.insert('', tk.END, values=(result['concurso'], result['data'], ', '.join(result['numeros'])))

    tree.pack(expand=True, fill='both')

    root.mainloop()

def display_most_common_numbers(most_common):
    numbers, counts = zip(*most_common)

    plt.figure(figsize=(10, 5))
    plt.bar(numbers, counts, color='blue')
    plt.xlabel('Números')
    plt.ylabel('Frequência')
    plt.title('Números Mais Frequentes na Lotofácil')
    plt.xticks(rotation=90)
    plt.show()

# Executa as funções
results = fetch_results(url)
save_results_to_json(results, 'lotofacil_results.json')
most_common_numbers = get_most_common_numbers(results)

# Exibe os resultados em uma interface gráfica
display_results(results)

# Exibe os números mais frequentes em um gráfico de barras
display_most_common_numbers(most_common_numbers)
