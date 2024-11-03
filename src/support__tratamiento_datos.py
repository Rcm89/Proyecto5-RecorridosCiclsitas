import os
import pandas as pd
from tqdm import tqdm

def dividir_dataframe(df):
    """
    Divide un DataFrame en segmentos basados en  la diferencia negativa entre filas en la columna de fechas.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que debe contener una columna llamada 'date' de tipo datetime para identificar los puntos de división.

    Returns
    -------
    list of pandas.DataFrame
        Lista de DataFrames divididos en segmentos, donde cada segmento corresponde a un período continuo de fechas
        crecientes. Cada división ocurre cuando la fecha actual es menor que la fecha anterior.

    Notes
    -----
    - La función identifica los índices en `df` donde la diferencia entre fechas consecutivas es negativa (disminución de fecha).
    - Luego divide el DataFrame en sub-DataFrames en esos puntos, de modo que cada sub-DataFrame contiene un intervalo continuo.
    - La columna 'date' debe estar en formato datetime para que `pd.Timedelta(0)` funcione correctamente en la comparación.
    """
    # Encontramos los índices donde hay diferencia de fechas negativa con respecto a la anterior. 
    # Es decir, ocurre una disminución en la fecha
    split_indices = df[df['date'].diff() < pd.Timedelta(0)].index

    # Creamos los DataFrames divididos en función de los índices de división
    dataframes_divididos = []
    start_idx = 0

    for idx in split_indices:
        dataframes_divididos.append(df.iloc[start_idx:idx])
        start_idx = idx

    dataframes_divididos.append(df.iloc[start_idx:])

    return dataframes_divididos