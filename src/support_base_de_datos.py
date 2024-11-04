import psycopg2
from psycopg2 import OperationalError, errorcodes, errors 
import numpy as np
import pandas as pd

import psycopg2
from psycopg2 import OperationalError, errorcodes
from psycopg2 import sql






def crear_basedatos(host,user,password,port,nombre_basedatos):
    conexion = psycopg2.connect(
        host=host,       
        user=user,      
        password=password, 
        port=port
    )


    conexion.autocommit = True  
    cursor = conexion.cursor()

    nombre_base_datos = nombre_basedatos

    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(nombre_base_datos)))
    except psycopg2.Error as e:
        print("Error de tipo:", e)

def establecer_conexion(host,user,password,port,nombre_basedatos):
    try: 
        conexion= psycopg2.connect(
            database= nombre_basedatos,
            user= user,
            password= password,
            host= host,
            port= port
        )
        conexion.autocommit = True
        
    except psycopg2.Error as e:
        return print(f"Ocurrió el error {e}")