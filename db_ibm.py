# -*- coding: utf-8 -*-

import ibm_db


class Db2sql():
    """
    db2 cursor handling
    """
    def __init__(self,cache,log):
        self.conn_string = cache
        self.log = log

        self.DATABASE = self.conn_string['DATABASE']
        self.HOSTNAME = self.conn_string['HOSTNAME']
        self.PORT     = self.conn_string['PORT']
        self.PROTOCOL = self.conn_string['PROTOCOL']
        self.UID      = self.conn_string['UID']
        self.PWD      = self.conn_string['PWD']
        self.CURRENTSCHEMA = self.conn_string['CURRENTSCHEMA']
        self.SECURITY = self.conn_string['SECURITY']

    def execute(self,sql,param=None,test=False):
        """
        If param is True, it returns a result for the cases of querys that return response,
        If param is None it does not return anything, for Inserts cases, updatesm deletes
        """
        conn_string =  f"DATABASE={self.DATABASE};HOSTNAME={self.HOSTNAME};PORT={self.PORT};PROTOCOL={self.PROTOCOL};UID={self.UID};PWD={self.PWD};CURRENTSCHEMA={self.CURRENTSCHEMA};SECURITY={self.SECURITY}"
        if test:
            return conn_string
        try:
            conn = ibm_db.connect(conn_string,"","")
            #ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_ON)
            if param is None:
                # TYPE FUNCTIONALITY INSERT,UPDATE,DELETE
                #sql = "INSERT INTO ASDA.TABKE VALUES ('?', ?, '?');"
                sql_preparado = ibm_db.prepare(conn, sql)
                ibm_db.execute(sql_preparado)
                #res = ibm_db.num_fields(stmt)
                ibm_db.commit(conn)
                return "ok"
            else:
                # QUERY, ONLY 1 ELEMENT RETURNS
                stmt = ibm_db.exec_immediate(conn, sql)
                res = ibm_db.fetch_both(stmt)
                #res = ibm_db.fetch_tuple(stmt) devolver solo los values
                return res
        except Exception as e:
            ibm_db.rollback(conn)
            msg = "Problems executing in sql " + str(e)
            #pdb.set_trace()
            self.log.error(msg)
        finally:
            ibm_db.close(conn)
