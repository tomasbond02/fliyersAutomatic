from PIL import Image, ImageDraw, ImageFont, ImageOps
from fastapi import UploadFile
from io import BytesIO, TextIOWrapper
import base64
import csv
import textwrap
import os


async def leer_csv_generic(file: UploadFile):
    file_bytes = await file.read()
    file_text_wrapper = TextIOWrapper(BytesIO(file_bytes), encoding='utf-8')
    diccionario = {}
    lector_csv = csv.reader(file_text_wrapper, delimiter=';')

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

def ver_data(mi_diccionario: list):
    titulos = mi_diccionario['\ufeffTITULO']
    nombres = mi_diccionario['NOMBRE']
    imagenes_cara = mi_diccionario['IMAGEN CARA']
    textos = mi_diccionario['TEXTO']
    dias = mi_diccionario['DIA']
    horarios = mi_diccionario['HORARIO']
    ubicaciones = mi_diccionario['UBICACION']    
    tipo = mi_diccionario['TIPO']

    return titulos, nombres, imagenes_cara, textos, dias, horarios, ubicaciones, tipo

def recortar_circulo(imagen: str):
    tamaño = imagen.size
    máscara = Image.new("L", tamaño, 0)
    dibujo = ImageDraw.Draw(máscara)
    dibujo.ellipse((0, 0, tamaño[0], tamaño[1]), fill=255)
    imagen_circular = ImageOps.fit(
        imagen, máscara.size, method=0, bleed=0.0, centering=(0.5, 0.5))
    imagen_circular.putalpha(máscara)
    return imagen_circular

def acomodarTexto(titulo: str, format: str):
    # Define la longitud mínima de palabra
    longitud_minima = 4

    # Separa el título en palabras
    palabras = titulo.split()
    # Cuenta el número de palabras
    numero_palabras = len(palabras)

    # Valida si todas las palabras cumplen la longitud mínima
    palabras_cumplen_longitud = all(
        len(palabra) >= longitud_minima for palabra in palabras)

    

    # Diccionario para mapear el número de palabras y si cumplen la longitud a un valor
    if format == 'historia':
        # Define el valor por defecto
        valor_por_defecto = 800
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
    elif format == 'feed':
        # Define el valor por defecto
        valor_por_defecto = 400
        valor_por_caso = {
            (4, True): 400,
            (3, True): 450,
            (2, True): 500,
            (1, True): 550,
            (4, False): 850,
            (3, False): 900,
            (2, False): 900,
            (1, False): 950

        }
    elif format == 'diploma':
        # Define el valor por defecto
        valor_por_defecto = 800
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
    # le deberia mandar esta parte por data
    print(numero_palabras,palabras_cumplen_longitud)
    # Busca el valor en el diccionario o usa el valor por defecto
    return valor_por_caso.get((numero_palabras, palabras_cumplen_longitud), valor_por_defecto)

def crear_carpeta(ruta_carpeta:str):
    try:
        os.makedirs(ruta_carpeta)
        return True
    except FileExistsError:
        return True
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
        return False

async def genericImagenCara(escala_cara:float, posicion_cara:int, fondo, cara):
    if cara:
        try:
            cara.file.seek(0)
            contents = await cara.read()
            imagen_cara = Image.open(BytesIO(contents))

            # Escala y mueve la imagen de la cara
            tamaño_cara_original = imagen_cara.size
            tamaño_cara = tuple(int(dim * escala_cara)
                                for dim in tamaño_cara_original)
            imagen_cara = imagen_cara.resize(tamaño_cara)

            # Recortar la imagen en forma circular
            imagen_cara_circular = recortar_circulo(imagen_cara)

            # Pegar la imagen circular en el fondo
            posición_final = (20 + posicion_cara[0], 20 + posicion_cara[1])
            fondo.paste(imagen_cara_circular,
                        posición_final, imagen_cara_circular)

        except FileNotFoundError as e:
            print(f"Error al cargar la imagen de cara: {e}")

def imagenes_a_base64(imagenes):
    imagenes_base64 = []
    for imagen in imagenes:
        # Convertir la imagen a modo RGB si es RGBA
        if imagen.mode == "RGBA":
            imagen = imagen.convert("RGB")
        with BytesIO() as output:
            imagen.save(output, format="JPEG")
            base64_str = base64.b64encode(output.getvalue()).decode()
            imagenes_base64.append(base64_str)
    return imagenes_base64

async def genericTemplate(
    background_image: UploadFile,
    faces: list[UploadFile],
    csv: UploadFile,
    fuente: str,
    x_posicion_cara: int,
    y_posicion_cara: int,
    escala_cara: float,
    escala_texto: int,
    x_titulo_wrapped: int,
    tamanio_fuente_titulo: int,
    width_titulo: int,
    x_nombre_wrapped: int,
    y_nombre_wrapped: int,
    tamanio_fuente_nombre: int,
    width_nombre: int,
    x_texto_wrapped: int,
    y_texto_wrapped: int,
    tamanio_fuente_texto: int,
    width_texto: int,
    x_dia_wrapped: int,
    y_dia_wrapped: int,
    tamanio_fuente_dia: int,
    width_dia: int,
    x_horario_wrapped: int,
    y_horario_wrapped: int,
    tamanio_fuente_horario: int,
    width_horario: int,
    x_ubicacion_wrapped: int,
    y_ubicacion_wrapped: int,
    tamanio_fuente_ubicacion: int,
    width_ubicacion: int,
    x_tipo_wrapped: int,
    y_tipo_wrapped: int,
    tamanio_fuente_tipo: int,
    width_tipo: int,
    format: str
):
    contents = await background_image.read()
    posicion_cara = (x_posicion_cara, y_posicion_cara)  # Cambia la posición de la imagen de la cara
    diccionario= await leer_csv_generic(csv)
    titulos, nombres, speackerImage, textos, dias, horarios, ubicaciones, tipo = ver_data(diccionario)
    responseImages = []
    crear_carpeta("carpeta_salida")
    
    for i in range(len(titulos)):
        fondo = Image.open(BytesIO(contents))
        draw = ImageDraw.Draw(fondo)#objeto draw
        pos_y = acomodarTexto(titulos[i], format)
        titulo_wrapped = textwrap.fill(
            titulos[i], width=width_titulo, break_long_words=False, replace_whitespace=False)
        draw.text((x_titulo_wrapped, pos_y), titulo_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_titulo * escala_texto)), fill="black")

        nombre_wrapped = textwrap.fill(
            nombres[i], width=width_nombre, break_long_words=False, replace_whitespace=False)
        draw.text((x_nombre_wrapped, y_nombre_wrapped), nombre_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_nombre * escala_texto)), fill="black")

        texto_wrapped = textwrap.fill(
            textos[i], width=width_texto, break_long_words=False, replace_whitespace=False)
        draw.text((x_texto_wrapped, y_texto_wrapped), texto_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_texto * escala_texto)), fill="black")

        dia_wrapped = textwrap.fill(
            dias[i], width=width_dia, break_long_words=False, replace_whitespace=False)
        draw.text((x_dia_wrapped, y_dia_wrapped), dia_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_dia * escala_texto)), fill="black")

        horario_wrapped = textwrap.fill(
            horarios[i], width=width_horario, break_long_words=False, replace_whitespace=False)
        draw.text((x_horario_wrapped, y_horario_wrapped),  horario_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_horario * escala_texto)), fill="black")

        ubicacion_wrapped = textwrap.fill(
            ubicaciones[i], width=width_ubicacion, break_long_words=False, replace_whitespace=False)
        draw.text((x_ubicacion_wrapped, y_ubicacion_wrapped), ubicacion_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_ubicacion * escala_texto)), fill="black")

        tipo_wrapped = textwrap.fill(
            tipo[i], width=width_tipo, break_long_words=False, replace_whitespace=False)
        draw.text((x_tipo_wrapped, y_tipo_wrapped), tipo_wrapped, font=ImageFont.truetype(
            fuente, int(tamanio_fuente_tipo * escala_texto)), fill="black",)
        
        face = None
        
        for j in faces:
            if j.filename == speackerImage[i]:
                face = j
            
        if face is not None:
            await genericImagenCara(escala_cara, posicion_cara, fondo, face)
        
        
        responseImages.append(fondo)
        
        
    return imagenes_a_base64(responseImages)
