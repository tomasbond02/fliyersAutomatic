from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import textwrap



#en esta funcion se compila la imagen
def imageCreation(texto:str, fuente:str, tamanioLetra:int, image:str, textColor, x:int, y:int, xInt:int, yInt:int, maxWidth:int):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    
    font = ImageFont.truetype(fuente, tamanioLetra)
    draw = ImageDraw.Draw(pil_image)
    
    textW, textH = draw.textssize(texto, font)
    textW = 0
    
    lineas = textwrap.wrap(texto, width=maxWidth//tamanioLetra)
    text_x = (image.shape[1] - textW) // x
    text_y = (image.shape[1] - textH) // y
    text_x = text_x + xInt
    text_y = text_y + yInt
    
    for linea in lineas:
        draw.text((text_x, text_y), linea, font=font, fill=textColor)
        text_y = text_x + 60
    
    image = np.asarray(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    imagenNp = np.array(image)
    
    return imagenNp


def enmascarar(img:str, mascara:str):
    imgM = cv2.bitwise_and(img, img, mask=mascara)
    
    return imgM

#en esta funcion se hace una mascara para la imagen a mostrar
def crearMascara(img:str, offset:str):
    h, w, c, = img.shape
    mascara1 = np.zeros(shape=(h,w), dtype='uint8')
    cv2.circle(mascara1, (int(w//2)), int(h//2), (3*offset), 255, -1)
    
    mascara = enmascarar(img, mascara1)
    
    return mascara
    

def cambiarFondo(img:str):
    colorNegro = [0,0,0]
    colorFondo = [255, 255, 255]
    
    mascara = cv2.inRange(img, np.array(colorNegro), np.array(colorFondo))
    
    imagen = np.copy(img)
    imagen[mascara !=0] = colorFondo
    
    return imagen
    