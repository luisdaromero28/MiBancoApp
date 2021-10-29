# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:58:50 2021

@author: CAP04
"""
from fastapi.testclient import TestClient
import pytest

import os
import json

from main import Maindb2
from modelo import modelo_ibm
from api import app

client = TestClient(app)
main = Maindb2

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'mocks', 'input.json')
FILE_RESPONSE = os.path.join(ROOT_FILE, 'mocks', 'response.json')
FILE_RESPONSE_FASTAPI = os.path.join(ROOT_FILE, 'mocks', 'response_fastapi.json')
FILE_RESPONSE_TEST_INSERT = os.path.join(ROOT_FILE, 'mocks', 'response_test_insert.json')

def json_input(file):
    """
    read input data json
    """
    with open (file,'rb') as file:
        data = json.load(file)
    return data


def test_data():
    """
    read input data json
    """
    data = json_input(FILE_INPUT)
    res = modelo_ibm(data)
    assert res == json_input(FILE_RESPONSE)


def test_response_model_ibm():
    """
    Test response model IBM
    """
    paramrecibe = json_input(FILE_INPUT)
    data = modelo_ibm(paramrecibe)
    assert type(data) == type({'test':'test'}) #VALIDAR


def test_insert_db2_ibm():
    """
    Test insert db2 ibm
    """
    data = json_input(FILE_RESPONSE_TEST_INSERT)
    db2 = Maindb2(data)
    insert = db2.insert()
    delete = db2.delete_test()
    assert insert == "insertOK"
    assert delete == "deleteOK"


@pytest.mark.parametrize('param,expected', [
    (json_input(FILE_INPUT),json_input(FILE_RESPONSE_FASTAPI))
])
def test_read_main_response(param,expected):
    """
    Test service api rest response
    """
    response = client.post('/scoring_conparameter/',json=param)
    assert response.json() == expected


@pytest.mark.parametrize('param', [
    (json_input(FILE_INPUT))
])
def test_read_main_status(param):
    """
    Test service api rest status
    """
    response = client.post('/scoring_conparameter/',json=param)
    assert response.status_code == 200


def test_string_coneccion():
    """
    Test string coneccion, json validate
    """
    bd = 'conn_db2'
    with open(f'conexion/{bd}.json') as f_in:
        json_str = f_in.read() 
    get_config = json.loads(json_str)
    assert type(get_config) == type({'test':'test'})
