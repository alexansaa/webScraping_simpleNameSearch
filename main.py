import os
import time
import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

base = 'https://www.gutenberg.org'
repositorio = base + '/browse/scores/top#books-last1'
directorio = 'libros'
names_file_name = 'libros_nombres.txt'

def salir():
    print("Saliendo...")
    # Add any exit code here if needed
    exit()

def descargar_archivos():
    print("Descargando archivos...")
    response = requests.get(repositorio)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')
    h2_element = soup.find('h2', text='Top 100 EBooks yesterday')
    book_list = h2_element.find_next('ol').find_all('a')

    if not os.path.exists('libros'):
        os.makedirs('libros')
    
    for book_link in book_list:
        book_url = base + book_link['href']
        book_response = requests.get(book_url)
        book_html = book_response.text
        book_soup = BeautifulSoup(book_html, 'html.parser')
        
        download_link = book_soup.find('a', title='Download', text='Plain Text UTF-8')
        if download_link:
            download_url = base + download_link['href']
            book_content = requests.get(download_url).text
            
            book_title = book_link.text.split('by')[0].strip()
            book_title_text_only = re.sub(r'[^a-zA-Z\s]', '', book_title)

            filename = os.path.join(directorio, f"{book_title_text_only}.txt")  # Modificación aquí
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(book_content)
            
            print(f'Descargado y guardado: {filename}')
        else:
            print(f'El libro "{book_link.text}" no está disponible en formato Plain Text UTF-8.')

    pass

def realizar_busqueda():
    print("Realizando búsqueda...")
    palabra_a_buscar = input("Ingrese la palabra que desea buscar: ")
    palabra_a_buscar.lower()

    archivos_con_palabra = []

    tiempo_inicial = time.time()

    for filename in os.listdir(directorio):
        if filename.endswith('.txt'):
            print("Buscando en {}".format(filename))
            with open(os.path.join(directorio, filename), 'r') as file:
                contenido = file.read().lower()
                # Busca la palabra en el contenido del archivo
                if palabra_a_buscar in contenido:
                    archivos_con_palabra.append(filename)

    print("FINALIZO LA BUSQUEDA")
    print("\n\n\n")

    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial

    if archivos_con_palabra:
        print("La palabra '{}' se encontró en los siguientes archivos:".format(palabra_a_buscar))
        for archivo in archivos_con_palabra:
            print(archivo)
    else:
        print("La palabra '{}' no se encontró en ningún archivo.".format(palabra_a_buscar))

    print("Tiempo de ejecución: {:.2f} segundos".format(tiempo_total))

    pass

def busqueda_avanzada():
    print("Realizando búsqueda avanzada...")
    file_matches = defaultdict(int)

    files = os.listdir(directory)

    pattern = re.compile(query, re.IGNORECASE)

    for file_name in files:
        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:
            content = file.read()

        matches = re.findall(pattern, content)

        file_matches[file_name] = len(matches)

    sorted_files = sorted(file_matches.items(), key=lambda x: x[1], reverse=True)

    return sorted_files

def obtener_nombres():
    names_file_name

    print("Obteniendo nombres de archivos...")
    response = requests.get(repositorio)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')
    h2_element = soup.find('h2', text='Top 100 EBooks yesterday')
    book_list = h2_element.find_next('ol').find_all('a')

    if not os.path.exists('libros'):
        os.makedirs('libros')
    
    for book_link in book_list:
        book_title = book_link.text.split('by')[0].strip()
        book_title = book_title + ".txt" + "\n"

        names_file_path = os.path.join(directorio, names_file_name)
        with open(names_file_path, 'a', encoding='utf-8') as f:
            f.write(book_title)
        print('Nombres de archivos guardados')

    pass

def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Descargar archivos")
    print("2. Realizar búsqueda")
    print("3. Búsqueda avanzada")
    print("4. Obtener Nombres")
    print("5. Salir")

def main():
    print("****Bienvenido****")
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            descargar_archivos()
        elif opcion == "2":
            realizar_busqueda()
        elif opcion == "3":
            busqueda_avanzada()
        elif opcion == "4":
            obtener_nombres()
        elif opcion == "5":
            salir()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
