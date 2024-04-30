import os
import time
import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

# importaciones DEBER 2
import operator

ops = {
    "AND": operator.and_,
    "OR": operator.or_,
    "NOT": operator.not_,
}
prior = {
    "AND": 1,
    "OR": 1,
    "NOT": 2,
}

base = 'https://www.gutenberg.org'
repositorio = base + '/browse/scores/top#books-last1'
directorio = 'libros'
names_file_name = 'libros_nombres.txt'

regExpresion = r'[^0-9a-zA-Z\s]+'

# variables de requerimiento DEBER 2
inverted_index = {}
libros = []

def salir():
    print("Saliendo...")
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
            book_title_text_only = re.sub(regExpresion, '', book_title)

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
            with open(os.path.join(directorio, filename), 'r', encoding='utf-8') as file:
                file_text = re.sub(regExpresion, '', file.read())
                contenido = file_text.lower()
                # Busca la palabra en el contenido del archivo
                if palabra_a_buscar in contenido:
                    archivos_con_palabra.append(filename)

    print("FINALIZO LA BUSQUEDA")
    print("---------------------------------")
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
    query = input("Ingrese la expresión regular que desea buscar: ")


    file_matches = defaultdict(int)

    files = os.listdir(directorio)

    pattern = re.compile(query, re.IGNORECASE)

    for file_name in files:
        with open(os.path.join(directorio, file_name), 'r', encoding='utf-8') as file:
            content = file.read()
        matches = re.findall(pattern, content)
        file_matches[file_name] = len(matches)
    sorted_files = sorted(file_matches.items(), key=lambda x: x[1], reverse=True)

    print("Los archivos que contienen la expresión regular son:")
    for file_name, matches in sorted_files:
        print(f"{file_name}: {matches} matches")

    return sorted_files

def obtener_nombres():
    print("Obteniendo nombres de archivos...")
    response = requests.get(repositorio)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')
    h2_element = soup.find('h2', text='Top 100 EBooks yesterday')
    book_list = h2_element.find_next('ol').find_all('a')
    
    for book_link in book_list:
        book_title = book_link.text.split('by')[0].strip()
        book_title_text_only = re.sub(regExpresion, '', book_title)
        book_title_text_only = book_title_text_only + ".txt" + "\n"

        names_file_path = os.path.join(names_file_name)
        with open(names_file_path, 'a', encoding='utf-8') as f:
            f.write(book_title_text_only)
        print('Nombres de archivos guardados')

    pass

def load_book_names():
    names_file_path = os.path.join(names_file_name)
    with open(names_file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def obtener_indice_invertido():
    print("Obteniendo índice invertido...")
    
    global libros
    for libro_id, libro in enumerate(libros):
        file = os.path.join(directorio, libro.strip())
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(regExpresion, '', content)
                words = content.split()
                for word in words:
                    global inverted_index
                    if word not in inverted_index:
                        inverted_index[word] = set()
                    inverted_index[word].add(libro_id)
        except:
            print(f"Error al abrir el archivo {file}. No existe o no se puede leer.")
            continue

    # print("imprimiendo indice invertido: ")
    # for key, value in inverted_index.items():
    #     print(key, ':', value)
    pass

# def parseEval(string):
#     content = string.split()
#     for priorMode in range(maxPrior+1):
#         print(content)
#         subParse = []
#         subParse = []
#         for ind,cont in enumerate(content):
#             if cont in ops:
#                 priorLev = prior[cont]
#                 if priorLev <= priorMode:
#                     condA = content[ind-1]
#                     condB = content[ind+1]
#                     subParse.append(ops[cont](condA,condB))
#                 else:
#                     subParse.append(cont)   
#         content = subParse
#     print(content)
#     return subParse[0]

def busqueda_matricial_con_operadores():
    print("Realizando búsqueda matricial con operadores...")
    print("ingrese las palabras a buscar separadas por espacios junto los operadores AND, OR, NOT (recuerde que NOT debe precederse con un OR o un AND)")
    # print("las prioridades de los operadores son NOT, AND, OR")
    query = input("Ingrese la expresion a buscar (ej: juan and pedro or not zapato): ")
    query = re.sub(r'[^\w\s]', '', query)
    tokens = re.findall(r'\b(?!and\b|or\b|not\b)\w+\b', query)
    content = re.findall(r'\b\w+\b|[()]|[and|or|not]+', query)

    cols = len(libros)
    rows = len(tokens)

    matrix = []

    for i, token in enumerate(tokens):
        tmp_row = [False for _ in range(cols)]
        if token in inverted_index:
            print("token in inverted_index: ", token)
            for j in inverted_index[token]:
                tmp_row[j] = True
        matrix.append(tmp_row)

    print(matrix)

    found_books = []

    for i in range(cols):
        token_names = tokens
        token_values = [matrix[j][i] for j in range(rows)]

        print("my token names: ", token_names)
        print("my token values: ", token_values)

        # token_map = {name: value for name, value in zip(token_names, token_values)}
        token_map = {name: value for name, value in zip(token_names, token_values)}
        print("my token map: ", token_map)

        content_temp = [token_map.get(token, token) for token in content]


        print("my content map: ", content_temp)

        expression = ' '.join(map(str, content_temp))
        result = eval(expression)
        if result:
            tpm_name = libros[i]
            tpm_name = tpm_name.rstrip("\n")
            found_books.append(tpm_name)

        # aqui se implementa el diccionario rankeado

    print("Los libros que cumplen con la expresión son:", found_books)

    return found_books

def deber_dos_menu():
    inMenuDeberDos = True
    while inMenuDeberDos:
        print("\n--- Menú Deber 2---")
        print("1. Obtener Indice Invertido")
        print("2. Realizar búsqueda matricial con operadores")
        print("3. Regresar al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            obtener_indice_invertido()
        elif opcion == "2":
            if(inverted_index == {}):
                print("Primero debe obtener el índice invertido!!!")
            else:
                print(busqueda_matricial_con_operadores())
        elif opcion == "3":
            inMenuDeberDos = False
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

    pass

def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Descargar archivos")
    print("2. Realizar búsqueda simple")
    print("3. Realizar búsqueda simple con ranqueo de archivos")
    print("4. Obtener Nombres de archivos")
    print("5. Metodos Deber 2")
    print("6. Salir")

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
            global libros
            libros = load_book_names()
            # print("Libros cargados")
            # for libro in libros:
            #     print(libro)

            if libros:
                deber_dos_menu()
            else:
                print("Primero debe descargar los archivos!!!")
        elif opcion == "6":
            salir()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
