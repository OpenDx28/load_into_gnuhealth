# load_into_gnuhealth

Este repositorio contiene los scripts necesarios para producir los datos requeridos para la creación de indicadores específicos.

## Estructura del repositorio 
En la carpeta principal de encuentra:
- Documento docker-compose.yaml para desplegar todos los servicios esenciales con una base de datos previamente poblada.
- __diseases.csv__ documento que traduce los nombres de las enfermedades según aparecen en DHIS2  a aquellas que coinciden en programa gnuhealth con sus códigos.
- __main.py__ generador de datos.
- __case_creator__ contiene las funciones para generar lso datos.

## Despliegue de Servicios

Usando Docker Compose, se levantarán los siguientes servicios:

- Base de datos con datos generados automáticamente por los scripts de este repositorio.
- Servidor Tryton.
- Cliente GNU Health.

### Construcción de Imágenes Docker:

1. Servidor Tryton:
``
docker build -t opendx/gnu_health https://github.com/OpenDx28/gnu-health-server-docker.git#new_demo
``

2. Interfaz Gráfica GNU Health:


``
docker build -t vnc-base https://github.com/OpenDx28/docker-vnc-base.git#:src
``

``
docker build -t gnu-hc --build-arg BASE_IMAGE="vnc-base:latest" https://github.com/OpenDx28/docker-gnu-hc.git#:src
``
3. Base de datos Postgres:
Esta imagen se descargará automáticamente al ejecutar el comando docker-compose up -d.


