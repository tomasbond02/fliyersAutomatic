from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv
import textwrap
import os

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
    

    return titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones, formato

def recortar_circulo(imagen:str):
    tamaño = imagen.size
    máscara = Image.new("L", tamaño, 0)
    dibujo = ImageDraw.Draw(máscara)
    dibujo.ellipse((0, 0, tamaño[0], tamaño[1]), fill=255)
    imagen_circular = ImageOps.fit(imagen, máscara.size, method=0, bleed=0.0, centering=(0.5, 0.5))
    imagen_circular.putalpha(máscara)
    return imagen_circular

def agregar_texto_a_foto(titulo:str, nombre:str, imagen_cara, texto, dia, horario, ubicacion, fondo_path, salida_path, posicion_cara, escala_cara, escala_texto):
    fondo = Image.open(fondo_path)
    draw = ImageDraw.Draw(fondo)

    # Cargar un tipo de letra TrueType (TTF) con el tamaño deseado
    font_size = 18  # Tamaño de fuente deseado

    font_size_texto = int(font_size * escala_texto)
    font_texto = ImageFont.truetype("arial.ttf", font_size_texto)

    titulo_wrapped = textwrap.fill(titulo, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((30, 20), titulo_wrapped, font=font_texto, fill="white")
    
    nombre_wrapped = textwrap.fill(nombre, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((40, 550), nombre_wrapped, font=font_texto, fill="white")
    
    texto_wrapped = textwrap.fill(texto, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((50, 20), texto_wrapped, font=font_texto, fill="white")
    
    dia_wrapped = textwrap.fill(dia, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((60, 20), dia_wrapped, font=font_texto, fill="white")

    horario_wrapped = textwrap.fill(horario, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((70, 20),  horario_wrapped, font=font_texto, fill="white")
    
    ubicacion_wrapped = textwrap.fill(ubicacion, width=2, break_long_words=False, replace_whitespace=False)
    draw.text((80, 20), ubicacion_wrapped, font=font_texto, fill="white")

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
    fondo_path = os.path.join("fondo1.jpeg")

    mi_diccionario = leer_csv(data)
    titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones, formato = ver_data(mi_diccionario)

    for i in range(len(titulos)):
        salida_path = f"filename_{i + 1}.png"  # Cambié a PNG para soportar transparencia
        if formato[i] == 'historia':
            # Ajusta estos valores según tus necesidades
            posicion_cara = (291, 392)  # Cambia la posición de la imagen de la cara
            escala_cara = 0.5  # Cambia la escala de la imagen de la cara
            escala_texto = 5  # Cambia la escala del texto
            print("este formato es de historia")
        elif formato[i] == 'post':
            # Ajusta estos valores según tus necesidades
            posicion_cara = (291, 392)  # Cambia la posición de la imagen de la cara
            escala_cara = 0.5  # Cambia la escala de la imagen de la cara
            escala_texto = 5  # Cambia la escala del texto
            print("este formato es de post")
        agregar_texto_a_foto(titulos[i], nombres[i], imagenes_cara[i], textos[i], dias[i], horarios[i], ubicaciones[i], fondo_path, salida_path, posicion_cara, escala_cara, escala_texto)

if __name__ == "__main__":
    main()