
# Simulador Cripto
    Este proyecto fue desarrollado como trabajo final del Bootcamp de KeepCoding "Aprende a Programar desde Cero (Full Stack Jr. )", Edición XXIII.  
    Se trata de una aplicación web que permite simular la compra, venta e intercambio de criptomonedas, registrar los movimientos y consultar en tiempo real el estado de la inversión con cotizaciones actualizadas mediante la API de CoinGecko.

---

## Tecnologías utilizadas

    - Python 3.11
    - Flask
    - HTML5 + CSS3
    - SQLite3
    - CoinGecko API
    - dotenv
    - requests

---

## Instalación

 1. Clonar el repositorio
 2. Crear y activar entorno virtual
 3. Instalar dependencias

## Clave API de CoinGecko
Esta app utiliza la API gratuita de CoinGecko.
 1. Regístrate en https://www.coingecko.com/es/developers
 2. Crea una clave API demo
 3. Crea un archivo .env en la raíz del proyecto con este contenido:
        COINGECKO_API_KEY=tu_clave_api_aquí

## Base de datos
    La aplicación utiliza SQLite como sistema de almacenamiento.
        1. Crear la base de datos manualmente (opcional)
            sqlite3 instance/database.db < schema.sql
       
        2. Si no ejecutas este paso, la base de datos se generará automáticamente al registrar el primer movimiento.

## Estructura de la tabla movimientos
   ### Estructura de la tabla `movimientos`

| Campo            | Tipo    | Descripción                                          |
|------------------|---------|------------------------------------------------------|
| `id`             | INTEGER | ID único del movimiento (autoincremental)            |
| `fecha`          | TEXT    | Fecha del movimiento (formato dd/mm/aaaa)            |
| `hora`           | TEXT    | Hora del movimiento (formato hh:mm:ss)               |
| `from_moneda`    | TEXT    | Moneda de origen (ej: EUR, BTC, ETH)                 |
| `cantidad_from`  | REAL    | Cantidad entregada                                   |
| `to_moneda`      | TEXT    | Moneda de destino                                    |
| `cantidad_to`    | REAL    | Cantidad recibida                                    |
| `valor_unitario` | REAL    | Valor de 1 unidad de `from_moneda` en `to_moneda`    |


## Ejecución de la aplicación
   1. ejecuta por terminal: flask run
   2. link: http://127.0.0.1:5000


## Funcionalidades de la aplicación
   ### / Página principal
    - Tabla con todos los movimientos registrados
    - Visualización clara de compras, ventas e intercambios

   ### /purchase Formulario de operación
    - Selección de monedas de origen y destino
    - Ingreso de cantidad y cálculo previo al envío
    - Registro del movimiento en base de datos
    - Permite:
        - Comprar cripto con euros
        - Vender cripto a euros
        - Intercambiar entre criptomonedas

   ### /status Estado de inversión
    - Muestra:
        - Total de euros invertidos
        - Euros recuperados
        - Euros atrapados en cripto
        - Valor actual de las criptomonedas (en tiempo real)
        - Ganancia o pérdida total
        
    - Detalle por criptomoneda: cantidad, cotización y valor en euros

## Autoría
    Florencia Noel Aldaya
    2025 - Proyecto final – KeepCoding Bootcamp | Aprende a Programar desde Cero (Full Stack Jr. ) | Edición XXIII


---






