from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv
import os

def leer_csv(nombre_archivo):
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

def ver_data(mi_diccionario):
    titulos = mi_diccionario['\ufeffTITULO']
    nombres = mi_diccionario['NOMBRE']
    imagenes_cara = mi_diccionario['IMAGEN CARA']
    textos = mi_diccionario['TEXTO']
    dias = mi_diccionario['DIA']
    horarios = mi_diccionario['HORARIO']
    ubicaciones = mi_diccionario['UBICACION']

    return titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones

def recortar_circulo(imagen):
    tamaño = imagen.size
    máscara = Image.new("L", tamaño, 0)
    dibujo = ImageDraw.Draw(máscara)
    dibujo.ellipse((0, 0, tamaño[0], tamaño[1]), fill=255)
    imagen_circular = ImageOps.fit(imagen, máscara.size, method=0, bleed=0.0, centering=(0.5, 0.5))
    imagen_circular.putalpha(máscara)
    return imagen_circular

def agregar_texto_a_foto(titulo, nombre, imagen_cara, texto, dia, horario, ubicacion, fondo_path, salida_path, posicion_cara, escala_cara, posicion_texto, escala_texto):
    fondo = Image.open(fondo_path)
    draw = ImageDraw.Draw(fondo)

    # Cargar un tipo de letra TrueType (TTF) con el tamaño deseado
    font_size = 18  # Tamaño de fuente deseado
    font = ImageFont.truetype("arial.ttf", font_size)

    font_size_texto = int(font_size * escala_texto)
    font_texto = ImageFont.truetype("arial.ttf", font_size_texto)

    draw.text((30, 20), titulo, font=font_texto, fill="white")
    
    draw.text((40, 20), nombre, font=font_texto, fill="white")
    
    draw.text((50, 20), texto, font=font_texto, fill="white")
    
    draw.text((60, 20), dia, font=font_texto, fill="white")
    
    draw.text((70, 20),  horario, font=font_texto, fill="white")
    
    draw.text((80, 20), ubicacion, font=font_texto, fill="white")

    if imagen_cara:
        imagen_cara_path = os.path.join("public", imagen_cara)
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

    fondo.save(salida_path)
def main():
    data = os.path.join("public", "data.csv")
    fondo_path = os.path.join("public", "fondo1.jpeg")

    mi_diccionario = leer_csv(data)
    titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones = ver_data(mi_diccionario)

    for i in range(len(titulos)):
        salida_path = f"filename_{i + 1}.png"  # Cambié a PNG para soportar transparencia
        # Ajusta estos valores según tus necesidades
        posicion_cara = (291, 272)  # Cambia la posición de la imagen de la cara
        escala_cara = 0.5  # Cambia la escala de la imagen de la cara
        posicion_texto = (20, 20)  # Cambia la posición del texto
        escala_texto = 5  # Cambia la escala del texto
        agregar_texto_a_foto(titulos[i], nombres[i], imagenes_cara[i], textos[i], dias[i], horarios[i], ubicaciones[i], fondo_path, salida_path, posicion_cara, escala_cara, posicion_texto, escala_texto)

if __name__ == "__main__":
    main()