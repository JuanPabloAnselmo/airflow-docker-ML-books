# Proyecto: Pipeline orquestado con Airflow para obtener información de libros relevantes de Mercado Libre

## Introducción
El proyecto se centra en la creación de un pipeline orquestado con Airflow, con el objetivo de obtener información sobre los libros más relevantes de Mercado Libre a través de su API. Este proceso se realiza mediante contenedores Docker para garantizar la portabilidad y la gestión eficiente de los recursos. Además se guarda la información en una base de datos PostgreSQL y se envia en cada corrida un mail con información de los diez principales libros.

## Objetivo
El objetivo principal del proyecto es implementar un flujo de trabajo automatizado que permita obtener datos actualizados sobre los libros más relevantes en Mercado Libre, almacenar estos datos en una base de datos PostgreSQL y, posteriormente, seleccionar los diez libros más relevantes para enviarlos por correo electrónico, incluyendo detalles como el título, la imagen, el precio, el enlace de compra y el vendedor asociado a cada libro.

## Tecnologías Utilizadas
1. **Airflow**: Utilizado para orquestar y programar las tareas del pipeline.
2. **Docker**: Para encapsular y desplegar el pipeline de manera eficiente y reproducible.
3. **Mercado Libre API**: Para obtener información actualizada sobre los libros más relevantes.
4. **PostgreSQL**: Base de datos utilizada para almacenar los datos recuperados de la API de Mercado Libre.
5. **SMTP Protocol**: Utilizado para enviar correos electrónicos con la información seleccionada.
6. **Python**: Principal lenguaje de programacion que se utiliza.

## Estructura del Pipeline
El pipeline se estructura en las siguientes etapas:

1. **Creación de base de datos**: Se crea base de datos en PostgreSQL para posterior almacenamiento
2. **Extracción de datos**: Utilizando la API de Mercado Libre para obtener información sobre los libros más relevantes.
3. **Almacenamiento en PostgreSQL**: Los datos extraídos se guardan en una base de datos PostgreSQL para su posterior procesamiento.
4. **Selección de los 10 libros más relevantes**: Selecciona los diez libros más relevantes de la base de datos basados en criterios específicos, como la popularidad o las calificaciones.
5. **Creación del correo electrónico**: Se genera un correo electrónico con los detalles de los libros seleccionados, incluyendo título, imagen, precio, enlace de compra y vendedor.
6. **Envío del correo electrónico**: Utilizando el protocolo SMTP, se envía el correo electrónico al destinatario especificado.

## Instrucciones de Uso

1. Modificar archivo .env con el respectivo mail del usuario, mail del destinatario y la app passwords que se utilizaran como variables de ambiente al levantar el contenedor
2. Levantar contenedor Docker mediante el archivo **docker-compose**
  - Abrir consola y dentro de la carpeta con los archivos utilizar comando:
```
docker-compose up airflow-init
```
   - Una vez finalizado, levandar el docker-compose:
```
docker compose up
```
Para mas información dejo estos links:
   -  [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
   -  [Running Airflow 2.0 with Docker in 5 mins](https://www.youtube.com/watch?v=aTaytcxy2Ck&t=526s&ab_channel=DatawithMarc)

3. Con el contenedor levantado, ingresar al webserver: [localhost](http://localhost:8080/)
   - **Usuario**: airflow | **Contraseña**: airflow
4. Conectarse a PostgreSQL. Seguir este video: [Airflow Connection connect to Postgres](https://www.youtube.com/watch?v=S1eapG6gjLU&t=249s&ab_channel=coder2j)
   - **Connection Id**: postgres_localhost
   - **Connection Type**: Postgres
   - **Host**: host.docker.internal
   - **Database**: postgres (O el nombre de la tabla que vayan a utilizar)
   - **Login**: airflow
   - **Password**: airflow
   
5. Correr el DAG "dag_ml_top_books_mail"




 
