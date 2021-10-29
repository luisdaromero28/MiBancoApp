from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from main import Maindb2
from modelo import modelo_ibm

app = FastAPI()

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'conexion', 'input.json')
FILE_APIKEY = os.path.join(ROOT_FILE, 'conexion', 'apikey.json')

#Iniciar programa
#uvicorn api:app --host="0.0.0.0" --port="5000" --reload


class Item(BaseModel):
    """
    Resultados de traducción
    define typing variables
    """
    TIPO_ID: str
    TIPO_PERSONA : int
    NUI : int
    NUM_IDENTIFICACION : int
    NOMBRES : str
    APELLIDOS : str
    RAZON_SOCIAL : str
    OFICINA : int
    CIIU : int
    FECHA_INGRESO : str
    CIUDAD_NACIMIENTO : str
    NACIONALIDAD : str
    CIUDAD_RESIDENCIA : str
    FECHA_NACIMIENTO : str
    PEP_NACIONAL : str
    PEP_EXTRANJERO : Optional[str] = None
    COD_CANAL_VINCULACION : str
    ACTIVOS : Optional[str] = None
    PASIVO : Optional[str] = None
    PATRIMONIO : Optional[str] = None
    INGRESOS : Optional[str] = None
    EGRESOS : Optional[str] = None
    OTROS_INGRESOS : Optional[str] = None
    ORIGEN_RECURSOS : str
    NOMBRE_VINCULO_FINANCIERA : str
    RESULTADO_LISTAS : str


def json_input():
    """
    read input data json
    """
    with open (FILE_INPUT,'rb') as file:
        data = json.load(file)
    return data['input_data'][0]


@app.post("/test_estructure_scoring/")
def post_model_ibm_test(item:Item):
    """
    Test structure json_input
    """
    return json_input()


@app.post("/scoring_conparameter/")
async def post_model_ibm(json=json_input()):
    """
    Execute model
    """
    data = modelo_ibm(json)
    db2 = Maindb2(data)
    res = db2.insert()
    return res,data
