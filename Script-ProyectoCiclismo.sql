-- Top 10 ediciones más largas
SELECT 
    carrera,
    edicion, 
    ano, 
    kilometros_totales
FROM 
    ediciones
ORDER BY 
    kilometros_totales DESC
LIMIT 10;

-- Top 10 ediciones más cortas

SELECT 
    carrera,
    edicion, 
    ano, 
    kilometros_totales
FROM 
    ediciones
ORDER BY 
    kilometros_totales ASC
LIMIT 10;

--Media en kilometros de las ediciones entre 2014 y 2024

SELECT 
    AVG(kilometros_totales) AS media_kilometros
FROM 
    ediciones
WHERE 
    ano BETWEEN 2015 AND 2024;

--Media de kilometros de las distintas ediciones por decada hasta 2010
   
SELECT 
    CASE 
        WHEN (ano / 10) * 10 <= 2010 THEN (ano / 10) * 10
        ELSE 2020
    END AS periodo,
    AVG(kilometros_totales) AS media_kilometros
FROM 
    ediciones
WHERE 
    ano <= 2024
GROUP BY 
    periodo
ORDER BY 
    periodo;
   
-- Maximo ganador de etpaas y numero de etapas ganadas en cada carrera
   
SELECT 
    carrera, 
    ganador_etapa, 
    COUNT(*) AS num_victorias
FROM 
    etapas
GROUP BY 
    carrera, ganador_etapa
HAVING 
    carrera = 'Giro' AND COUNT(*) = (
        SELECT MAX(num_victorias) 
        FROM (
            SELECT 
                COUNT(*) AS num_victorias
            FROM 
                etapas
            WHERE 
                carrera = 'Giro'
            GROUP BY 
                ganador_etapa
        ) AS subquery
    )
UNION
SELECT 
    carrera, 
    ganador_etapa, 
    COUNT(*) AS num_victorias
FROM 
    etapas
GROUP BY 
    carrera, ganador_etapa
HAVING 
    carrera = 'Tour' AND COUNT(*) = (
        SELECT MAX(num_victorias) 
        FROM (
            SELECT 
                COUNT(*) AS num_victorias
            FROM 
                etapas
            WHERE 
                carrera = 'Tour'
            GROUP BY 
                ganador_etapa
        ) AS subquery
    )
UNION
SELECT 
    carrera, 
    ganador_etapa, 
    COUNT(*) AS num_victorias
FROM 
    etapas
GROUP BY 
    carrera, ganador_etapa
HAVING 
    carrera = 'Vuelta' AND COUNT(*) = (
        SELECT MAX(num_victorias) 
        FROM (
            SELECT 
                COUNT(*) AS num_victorias
            FROM 
                etapas
            WHERE 
                carrera = 'Vuelta'
            GROUP BY 
                ganador_etapa
        ) AS subquery
    );


-- Calcular el total de kilometros contrarreloj y el porcentaje de kilometros contrarreloj sobre el total en todas las ediciones de Giro, Tour y Vuelta
   
SELECT 
    e.carrera,
    e.edicion,
    e.ano,
    e.kilometros_totales,
    COALESCE(SUM(CASE WHEN et.tipo_etapa IN ('TTT', 'ITT') THEN et.distancia ELSE 0 END), 0) AS km_crono,
    (COALESCE(SUM(CASE WHEN et.tipo_etapa IN ('TTT', 'ITT') THEN et.distancia ELSE 0 END), 0) * 100.0 / e.kilometros_totales) AS porcentaje_crono
FROM 
    ediciones e
LEFT JOIN 
    etapas et
ON 
    e.id = et.edicion_id
WHERE 
    e.carrera IN ('Giro', 'Tour', 'Vuelta')
GROUP BY 
    e.carrera, e.edicion, e.ano, e.kilometros_totales
ORDER BY 
    e.carrera, e.ano;
