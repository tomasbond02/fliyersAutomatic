from typing import Union, List
from fastapi import FastAPI, UploadFile
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/generar")
def generar_imagen(
    background_image: UploadFile,
    speackerImage: List[UploadFile],
    csv: UploadFile,
    fuente:str,
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
):
    # Aquí puedes realizar las operaciones que necesites con los parámetros recibidos
    return "ok"