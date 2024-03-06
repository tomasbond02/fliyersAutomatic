from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv
import textwrap
import os
import time

def leer_csv(nombre_archivo:str):
    diccionario = {}
    with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')
        
        # Obtén los encabezados (nombres de las columnas)
        encabezados = next(lector_csv)
        
        # Inicializa el diccionario con listas vacías para cada columna
        for encabezado in encabezados:
            diccionario[encabezado] = []

        # Lee el resto del archivo y almacena los datos en el diccionario
        for fila in lector_csv:
            for encabezado, valor in zip(encabezados, fila):
                diccionario[encabezado].append(valor)

    return diccionario

def ver_data(mi_diccionario:list):
    titulos = mi_diccionario['\ufeffTITULO']
    nombres = mi_diccionario['NOMBRE']
    imagenes_cara = mi_diccionario['IMAGEN CARA']
    textos = mi_diccionario['TEXTO']
    dias = mi_diccionario['DIA']
    horarios = mi_diccionario['HORARIO']
    ubicaciones = mi_diccionario['UBICACION']
    formato = mi_diccionario['FORMATO']
    tipo = mi_diccionario['TIPO']
    

    return titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones, formato, tipo

def recortar_circulo(imagen:str):
    tamaño = imagen.size
    máscara = Image.new("L", tamaño, 0)
    dibujo = ImageDraw.Draw(máscara)
    dibujo.ellipse((0, 0, tamaño[0], tamaño[1]), fill=255)
    imagen_circular = ImageOps.fit(imagen, máscara.size, method=0, bleed=0.0, centering=(0.5, 0.5))
    imagen_circular.putalpha(máscara)
    return imagen_circular

def separarTitulo(titulo:str):
    # Define la longitud mínima de palabra
    longitud_minima = 4

    # Separa el título en palabras
    palabras = titulo.split()

    # Cuenta el número de palabras
    numero_palabras = len(palabras)

    # Valida si todas las palabras cumplen la longitud mínima
    palabras_cumplen_longitud = all(len(palabra) >= longitud_minima for palabra in palabras)

    # Define el valor por defecto
    valor_por_defecto = None

    # Diccionario para mapear el número de palabras y si cumplen la longitud a un valor
    valor_por_caso = {
        (4, True): 800,
        (3, True): 850,
        (2, True): 900,
        (1, True): 950,
        (4, False): 850,
        (3, False): 900,
        (2, False): 900,
        (1, False): 950
        
    }

    # Busca el valor en el diccionario o usa el valor por defecto
    return valor_por_caso.get((numero_palabras, palabras_cumplen_longitud), valor_por_defecto)

def agregar_texto_a_foto_feed(titulo:str, nombre:str, imagen_cara, texto, dia, horario, ubicacion, tipo, fondo_path, salida_path, posicion_cara, escala_cara, escala_texto):
    fondo = Image.open(fondo_path)
    draw = ImageDraw.Draw(fondo)
    
    fuente = "arial.ttf"

    titulo_wrapped = textwrap.fill(titulo, width=20, break_long_words=False, replace_whitespace=False)
    draw.text((100, 450), titulo_wrapped, font=ImageFont.truetype(fuente, int(20 * escala_texto)), fill="black")
    
    nombre_wrapped = textwrap.fill(nombre, width=10, break_long_words=False, replace_whitespace=False)
    draw.text((750, 200), nombre_wrapped, font=ImageFont.truetype(fuente, int(10 * escala_texto)), fill="black")
    
    texto_wrapped = textwrap.fill(texto, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((100, 90), texto_wrapped, font=ImageFont.truetype(fuente, int(10 * escala_texto)), fill="black")
    
    dia_wrapped = textwrap.fill(dia, width=20, break_long_words=False, replace_whitespace=False)
    draw.text((100, 750), dia_wrapped, font=ImageFont.truetype(fuente, int(13 * escala_texto)), fill="black")

    horario_wrapped = textwrap.fill(horario, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((100, 800),  horario_wrapped, font=ImageFont.truetype(fuente, int(13 * escala_texto)), fill="black")
    
    ubicacion_wrapped = textwrap.fill(ubicacion, width=30, break_long_words=False, replace_whitespace=False)
    draw.text((100, 850), ubicacion_wrapped, font=ImageFont.truetype(fuente, int(13 * escala_texto)), fill="black")
    
    tipo_wrapped = textwrap.fill(tipo, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((100, 185), tipo_wrapped, font=ImageFont.truetype(fuente, int(12 * escala_texto)), fill="black",)

    if imagen_cara:
        imagen_cara_path = os.path.join("imgSpeacker", imagen_cara)
        try:
            imagen_cara = Image.open(imagen_cara_path)

            # Escala y mueve la imagen de la cara
            tamaño_cara_original = imagen_cara.size
            tamaño_cara = tuple(int(dim * escala_cara) for dim in tamaño_cara_original)
            imagen_cara = imagen_cara.resize(tamaño_cara)

            # Recortar la imagen en forma circular
            imagen_cara_circular = recortar_circulo(imagen_cara)

            # Pegar la imagen circular en el fondo
            posición_final = (20 + posicion_cara[0], 20 + posicion_cara[1])
            fondo.paste(imagen_cara_circular, posición_final, imagen_cara_circular)

        except FileNotFoundError as e:
            print(f"Error al cargar la imagen de cara: {e}")

    salida_path = os.path.join("carpeta_salida", salida_path)
    fondo.save(salida_path)
    
def agregar_texto_a_foto_historia(titulo:str, nombre:str, imagen_cara, texto, dia, horario, ubicacion, tipo, fondo_path, salida_path, posicion_cara, escala_cara, escala_texto):
    fondo = Image.open(fondo_path)
    draw = ImageDraw.Draw(fondo)
    
    fuente = "arial.ttf"
    
    pos_y = separarTitulo(titulo)

    titulo_wrapped = textwrap.fill(titulo, width=10, break_long_words=False, replace_whitespace=False)
    draw.text((300, pos_y), titulo_wrapped, font=ImageFont.truetype(fuente, int(27 * escala_texto)), fill="black")
    
    nombre_wrapped = textwrap.fill(nombre, width=10, break_long_words=False, replace_whitespace=False)
    draw.text((1050, 500), nombre_wrapped, font=ImageFont.truetype(fuente, int(10 * escala_texto)), fill="black")
    
    texto_wrapped = textwrap.fill(texto, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((300, 500), texto_wrapped, font=ImageFont.truetype(fuente, int(10 * escala_texto)), fill="black")
    
    dia_wrapped = textwrap.fill(dia, width=20, break_long_words=False, replace_whitespace=False)
    draw.text((300, 1500), dia_wrapped, font=ImageFont.truetype(fuente, int(18 * escala_texto)), fill="black")

    horario_wrapped = textwrap.fill(horario, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((300, 1600),  horario_wrapped, font=ImageFont.truetype(fuente, int(18 * escala_texto)), fill="black")
    
    ubicacion_wrapped = textwrap.fill(ubicacion, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((300, 1700), ubicacion_wrapped, font=ImageFont.truetype(fuente, int(18 * escala_texto)), fill="black")
    
    tipo_wrapped = textwrap.fill(tipo, width=19, break_long_words=False, replace_whitespace=False)
    draw.text((300, 610), tipo_wrapped, font=ImageFont.truetype(fuente, int(10 * escala_texto)), fill="black",)

    if imagen_cara:
        imagen_cara_path = os.path.join("imgSpeacker", imagen_cara)
        try:
            imagen_cara = Image.open(imagen_cara_path)

            # Escala y mueve la imagen de la cara
            tamaño_cara_original = imagen_cara.size
            tamaño_cara = tuple(int(dim * escala_cara) for dim in tamaño_cara_original)
            imagen_cara = imagen_cara.resize(tamaño_cara)

            # Recortar la imagen en forma circular
            imagen_cara_circular = recortar_circulo(imagen_cara)

            # Pegar la imagen circular en el fondo
            posición_final = (20 + posicion_cara[0], 20 + posicion_cara[1])
            fondo.paste(imagen_cara_circular, posición_final, imagen_cara_circular)

        except FileNotFoundError as e:
            print(f"Error al cargar la imagen de cara: {e}")

    salida_path = os.path.join("carpeta_salida", salida_path)
    fondo.save(salida_path)
#######################################################################################################################################
    
def main():
    data = os.path.join( "data.csv")
    fondo_path = os.path.join("fondo.jpg")

    mi_diccionario = leer_csv(data)
    titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones, formato, tipo = ver_data(mi_diccionario)

    for i in range(len(titulos)):
        salida_path = f"filename_{i + 1}.png"  # Cambié a PNG para soportar transparencia
        if formato[i] == 'historia':
            # Ajusta estos valores según tus necesidades
            fondo_path = os.path.join("fondoHistoria.jpg")
            posicion_cara = (1000, 50)  # Cambia la posición de la imagen de la cara
            escala_cara = 0.5  # Cambia la escala de la imagen de la cara
            escala_texto = 5  # Cambia la escala del texto
            print("este formato es de historia")
            agregar_texto_a_foto_historia(titulos[i], nombres[i], imagenes_cara[i], textos[i], dias[i], horarios[i], ubicaciones[i], tipo[i], fondo_path, salida_path, posicion_cara, escala_cara, escala_texto)
        elif formato[i] == 'post':
            # Ajusta estos valores según tus necesidades
            fondo_path = os.path.join("fondoFeed.png")
            posicion_cara = (790, 10)  # Cambia la posición de la imagen de la cara
            escala_cara = 0.2  # Cambia la escala de la imagen de la cara
            escala_texto = 4  # Cambia la escala del texto
            print("este formato es de post")
            agregar_texto_a_foto_feed(titulos[i], nombres[i], imagenes_cara[i], textos[i], dias[i], horarios[i], ubicaciones[i], tipo[i], fondo_path, salida_path, posicion_cara, escala_cara, escala_texto)
    print("el programa se serrara en 60 segundos...")
    

if __name__ == "__main__":
    main()
    time.sleep(60)