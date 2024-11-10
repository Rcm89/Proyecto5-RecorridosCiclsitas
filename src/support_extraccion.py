import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def escrapeo_wikipedia(lista_de_carreras):
    """
    Extrae datos estadísticos de Wikipedia para una lista de carreras y guarda cada tabla en archivos CSV.

    Parameters
    ----------
    lista_de_carreras : list of str
        Lista de nombres de carreras para las que se desea extraer datos estadísticos de Wikipedia.

    Returns
    -------
    list of pandas.DataFrame
        Lista de DataFrames, cada uno con los datos estadísticos extraídos de una tabla en Wikipedia para cada carrera.
    
    Notes
    -----
    - La función construye una URL de Wikipedia para cada carrera en `lista_de_carreras` y utiliza BeautifulSoup para
      extraer la tabla con clase 'wikitable'.
    - Si se encuentra una tabla en la página, la función guarda los datos en un DataFrame, lo exporta a un archivo CSV
      en la ruta '../datos/datos_wikipedia/datos_originales' y agrega el DataFrame a `lista_dfs`.
    - Si no se encuentra una tabla, la carrera correspondiente no se incluye en el resultado.
    """
    ruta_datos = '../datos/datos_wikipedia/datos_originales'
    os.makedirs(ruta_datos, exist_ok=True)

    lista_dfs = []
    # Iteramos sobre cada una de las arreras de lista_de_carreras
    for carrera in lista_de_carreras:
        url = 'https://es.wikipedia.org/wiki/Anexo:Datos_estad%C3%ADsticos_' + carrera

        # Extraemos con Beautiful Soup la tabla de la url de arriba y la guardamos en un DataFrame
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        tabla = soup.find('table', {'class': 'wikitable'})

        # Verificamos que se ha encontrado una tabla en la página
        if tabla:
            encabezados = [encabezado.text.strip() for encabezado in tabla.find_all('th')]

            filas = []
            for fila in tabla.find_all('tr')[1:]:
                celdas = fila.find_all(['td', 'th'])
                celdas_text = [celda.text.strip() for celda in celdas]
                filas.append(celdas_text)

            df = pd.DataFrame(filas, columns=encabezados)

            # Definimos la ruta y el nombre del archivo CSV
            nombre_archivo = f'df_{carrera}.csv'
            ruta_archivo = os.path.join(ruta_datos, nombre_archivo)

            # Guardamos el DataFrame en un archivo CSV
            df.to_csv(ruta_archivo, index=False)

            # Agregamos el DataFrame a la lista
            lista_dfs.append(df)
    
    return lista_dfs


def cargar_datos_wikipedia():
    """
    Carga archivos CSV desde una carpeta específica y almacena cada archivo en un DataFrame dentro de un diccionario.

    Returns
    -------
    dict
        Un diccionario donde cada clave es el nombre del archivo sin la extensión `.csv` y cada valor es un 
        DataFrame con los datos cargados del archivo correspondiente.

    Notes
    -----
    - La función busca archivos CSV en la ruta `../datos/datos_wikipedia/datos_limpiados`.
    - Si se encuentra un archivo CSV, se carga en un DataFrame, y el DataFrame se almacena en `diccionario_dataframes`
      con una clave derivada del nombre del archivo.
    - La primera columna de cada archivo se utiliza como índice en el DataFrame.
    """
    # Ruta de la carpeta donde están los archivos CSV
    ruta_datos = '../datos/datos_wikipedia/datos_limpiados'

    # Diccionario para almacenar los DataFrames
    diccionario_dataframes = {}

    # Iteramos sobre cada archivo en la carpeta
    for archivo in os.listdir(ruta_datos):
        if archivo.endswith('.csv'):
            clave_df = archivo.replace('.csv', '')
            ruta_archivo = os.path.join(ruta_datos, archivo)
            df = pd.read_csv(ruta_archivo)
            diccionario_dataframes[clave_df] = df
    return diccionario_dataframes


def extrer_info_api_procyclingstats(lista_ediciones_tres_carreras):
    """
    Extrae información detallada de las etapas de carreras de ciclismo desde la API de ProCyclingStats para las ediciones especificadas.

    Parameters
    ----------
    lista_ediciones_tres_carreras : list of list of int
        Lista que contiene sublistas de años para tres carreras principales (Giro d'Italia, Tour de France, Vuelta a España),
        en el siguiente orden: [[años del Giro], [años del Tour], [años de la Vuelta]].

    Returns
    -------
    list of dict
        Una lista de diccionarios, donde cada diccionario contiene la información procesada de una etapa de carrera.

    Notes
    -----
    - La función itera sobre cada carrera y año en `lista_ediciones_tres_carreras`, construyendo una URL específica
      para cada carrera y año, y luego obtiene información detallada de cada etapa.
    - Utiliza `Race` para obtener la carrera y `Stage` para analizar cada etapa.
    - Captura y maneja errores para etapas o años donde los datos no están disponibles o hay problemas de análisis.
    - Imprime mensajes de error si no encuentra datos para un año específico o si ocurre un error en una etapa.
    """
   
    lista_informacion = []

    for i, lista_ediciones in enumerate(tqdm(lista_ediciones_tres_carreras)):
        for anio in lista_ediciones:
            try:
                # Selecciona la carrera según el índice
                if i == 0:
                    race = Race(f"race/giro-d-italia/{anio}")
                elif i == 1:
                    race = Race(f"race/tour-de-france/{anio}")
                elif i == 2:
                    race = Race(f"race/vuelta-a-espana/{anio}")

                if race.html is None:
                    print(f"No se encontró la información para el año {anio}. Pasamos al siguiente")
                    continue

                # Obtener y procesar cada etapa de la carrera
                for etapa in race.stages():
                    try:
                        stage = Stage(etapa['stage_url'])
                        parsed_data = stage.parse()
                        lista_informacion.append(parsed_data)
                    except AttributeError as e:
                        print(f"Error al analizar la etapa en el año {anio}: {e}")
                    except Exception as e:
                        print(f"Error inesperado al analizar la etapa en el año {anio}: {e}")

            except AttributeError as e:
                print(f"Error al obtener datos para el año {anio}: {e}")
            except Exception as e:
                print(f"Error inesperado para el año {anio}: {e}")
        
    return lista_infomacion
    
