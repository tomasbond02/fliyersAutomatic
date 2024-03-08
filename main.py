from typing import Union, List, Annotated
from fastapi import FastAPI, UploadFile, Form, File
from buildTemplate import genericTemplate

app = FastAPI(
    timeout=30
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/generar")
async def generar_imagen(
    background_image: UploadFile,
    faces: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
    csv: UploadFile,
    fuente:str = Form(""),
    x_posicion_cara: int = Form(0),
    y_posicion_cara: int = Form(0),
    escala_cara: float = Form(0),
    escala_texto: int = Form(0),
    x_titulo_wrapped: int = Form(0),
    tamanio_fuente_titulo: int = Form(0),
    width_titulo: int = Form(0),
    x_nombre_wrapped: int = Form(0),
    y_nombre_wrapped: int = Form(0),
    tamanio_fuente_nombre: int = Form(0),
    width_nombre: int = Form(0),
    x_texto_wrapped: int = Form(0),
    y_texto_wrapped: int = Form(0),
    tamanio_fuente_texto: int = Form(0),
    width_texto: int = Form(0),
    x_dia_wrapped: int = Form(0),
    y_dia_wrapped: int = Form(0),
    tamanio_fuente_dia: int = Form(0),
    width_dia: int = Form(0),
    x_horario_wrapped: int = Form(0),
    y_horario_wrapped: int = Form(0),
    tamanio_fuente_horario: int = Form(0),
    width_horario: int = Form(0),
    x_ubicacion_wrapped: int = Form(0),
    y_ubicacion_wrapped: int = Form(0),
    tamanio_fuente_ubicacion: int = Form(0),
    width_ubicacion: int = Form(0),
    x_tipo_wrapped: int = Form(0),
    y_tipo_wrapped: int = Form(0),
    tamanio_fuente_tipo: int = Form(0),
    width_tipo: int = Form(0),
):
    return await genericTemplate(background_image, faces,csv, fuente, x_posicion_cara, y_posicion_cara, escala_cara, escala_texto, x_titulo_wrapped, tamanio_fuente_titulo, width_titulo, x_nombre_wrapped, y_nombre_wrapped, tamanio_fuente_nombre, width_nombre, x_texto_wrapped, y_texto_wrapped, tamanio_fuente_texto, width_texto, x_dia_wrapped,y_dia_wrapped,tamanio_fuente_dia,width_dia,x_horario_wrapped,y_horario_wrapped,tamanio_fuente_horario,width_horario,x_ubicacion_wrapped, y_ubicacion_wrapped, tamanio_fuente_ubicacion, width_ubicacion, x_tipo_wrapped, y_tipo_wrapped, tamanio_fuente_tipo, width_tipo)