{{ config(materialized='view') }}

SELECT 
    MAX(precio_compra) - MIN(precio_compra) AS variacion_compra,
    MAX(precio_venta) - MIN(precio_venta) AS variacion_venta
FROM 
    {{source('poker', 'dollarblue')}}
WHERE 
    fecha >= DATE(NOW()) - INTERVAL '7 days'
