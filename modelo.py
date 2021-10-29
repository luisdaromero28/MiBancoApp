# -*- coding: utf-8 -*-

import json
import requests
import os
import logging

logging.basicConfig(level=10, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename='log.log', filemode='w')

log = logging.getLogger('')

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'conexion', 'input.json')
FILE_APIKEY = os.path.join(ROOT_FILE, 'conexion', 'apikey.json')

def json_input():
    """
    read input data json
    """
    try:
        with open (FILE_INPUT,'rb') as file:
            data = json.load(file)
        return data['input_data'][0] 
    except Exception as e:
        msg = "Problemas para leer input: {FILE_INPUT} message {e}"
        log.error(msg)


def api_key():
    """
    read input data json
    """
    try:
        with open (FILE_APIKEY,'rb') as file:
            data = json.load(file)
        return data['apikey']
    except Exception as e:
        msg = "Problemas para leer input: {FILE_INPUT} message {e}"
        log.error(msg)


def modelo_ibm(json):
    """
    generate token and run model.
    """
    API_KEY = api_key()
    try:
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        payload_scoring = {"input_data": [json_input()]}
    except Exception as e:
        msg = "Problems generating ibm token " + str(e)
        log.error(msg)
        
    #header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    #payload_scoring = {"input_data": [json]}

    try:
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/083217b1-aa8c-4a81-bc12-4e089f897ca1/predictions?version=2021-10-07&version=2021-10-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        res = response_scoring.json()
    except Exception as e:
        msg = "Problems response scoring " + str(e)
        log.error(msg)
    return res
