import cv2
from codificacion import *


def titulo(imgFondo:str, texto:str):
    #caracteristicas del titulo a agregar
    font = "C:\Windows\Fonts\\arial.ttf"
    tamanioLetra = 160
    colorLetra = (0, 0, 0)
    x = 3
    y = 3
    xInt = -200
    yInt = -400
    maxWidth = 2000
    
    imagen = imageCreation(texto, font, tamanioLetra, imgFondo, colorLetra, x, y, xInt, yInt, maxWidth)
    
    return imagen

def texto(imgFondo:str, texto:str):
    #caracteristicas del texto a agregar
    font = "C:\Windows\Fonts\\arial.ttf"
    tamanioLetra = 160
    colorLetra = (0, 0, 0)
    x = 3
    y = 3
    xInt = -200
    yInt = -400
    maxWidth = 2000
    
    imagen = imageCreation(texto, font, tamanioLetra, imgFondo, colorLetra, x, y, xInt, yInt, maxWidth)
    
    return imagen

def nombre(imgFondo:str, texto:str):
    #caracteristicas del nombre a agregar
    font = "C:\Windows\Fonts\\arial.ttf"
    tamanioLetra = 160
    colorLetra = (0, 0, 0)
    x = 3
    y = 3
    xInt = -200
    yInt = -400
    maxWidth = 2000
    
    imagen = imageCreation(texto, font, tamanioLetra, imgFondo, colorLetra, x, y, xInt, yInt, maxWidth)
    
    return imagen


def subtitulo(imgFondo:str, texto:str):
    #caracteristicas del sbutitlo a agregar
    font = "C:\Windows\Fonts\\arial.ttf"
    tamanioLetra = 160
    colorLetra = (0, 0, 0)
    x = 3
    y = 3
    xInt = -200
    yInt = -400
    maxWidth = 2000
    
    imagen = imageCreation(texto, font, tamanioLetra, imgFondo, colorLetra, x, y, xInt, yInt, maxWidth)
    
    return imagen

def fotoImg(fondo:str, img:str):
    #leo la imagen
    
    rostro = cv2.imread(img)
    
    #escalo la imagen
    rostroEscalado = cv2.resize(rostro, (200, 200))
    
    #recorto la zona del fondo donde quiero que este la imagen
    parteFondo = fondo[1050: 1250, 550:750]
    
    mascara = crearMascara(rostroEscalado, 50)
    
    #junto todo
    
    imagen = cv2.addWeighted(src1=parteFondo, alpha=0, src2=mascara, beta=1, gamma=0)
    fondo[1050: 1250, 550:750] = imagen
    
    