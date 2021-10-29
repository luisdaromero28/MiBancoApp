# -*- coding: utf-8 -*-

import json
import logging
from db_ibm import Db2sql

logging.basicConfig(level=10, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename='log.log', filemode='w')

class Maindb2:
    def __init__(self,data):
        self.data = data
        self.log = logging.getLogger('')

    def get_config(self,bd):
        try:
          with open('conexion/'+bd+'.json') as f_in:
            json_str = f_in.read()
            return json.loads(json_str)
        except Exception as e:
          msg = "Problems get_config " + str(e)
          self.log.error(msg)
          return "error"
    
    def connection(self):
      """
      connection db2
      """
      return Db2sql(self.get_config('conn_db2'),self.log)
        
    def insert(self):
        try:
          sql = self.connection()
        except Exception as e:
          msg = "Problems string connection " + str(e)
          self.log.error(msg)
        
        #transformar el json
        values = self.data['predictions'][0]['values'][0]
        insert = f"INSERT INTO KFJ27317.TABLA_PRUEBA (NUIP,SCORE,CALIFICACION) VALUES ('{values[0]}',{values[1]},'{values[2]}');"
        sql.execute(insert)
        return "insertOK"

    def listar(self,query):
        try:
          sql = self.connection()
        except Exception as e:
          msg = "Problems string connection " + str(e)
          self.log.error(msg)
        dictionary = sql.execute(query,param=True)
        print(dictionary)
        return dictionary
    
    def delete_test(self):
        """
        Delete row test
        """
        try:
          sql = self.connection()        
          delete = "DELETE FROM KFJ27317.TABLA_PRUEBA WHERE CALIFICACION = 'mibancotestinsertdb2ibm'"
          sql.execute(delete)
          return "deleteOK"
        except Exception as e:
            msg = "Problems string connection " + str(e)
            self.log.error(msg)
            return "error"