import logging
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendMail(data):
    servidor_smtp = 'smtp.gmail.com'
    puerto = 587
    usuario = os.environ.get('USUARIO_MAIL') # Colocar mail desde donde se enviara
    contraseña = os.environ.get('PASSWORD_MAIL') # Contraseña app de GMAIL
    destinatario = os.environ.get('DESTINATARIO_MAIL')# Destinatario
    
        # Asunto del correo
    asunto = f'Top 10 libros más relevantes de Mercado Libre ({datetime.now().strftime("%Y-%m-%d")})'

    # Construir contenido HTML del correo con la información de todos los libros
    contenido = f"<html><body><h1>Top 10 libros más relevantes de Mercado Libre ({datetime.date(datetime.today())})</h1>"  
    for libro in data:
        contenido += f"""
        <h1>{libro[1]}</h1>
        <img src="{libro[3]}" alt="imagen">
        <h2>Precio: ${libro[2]}</h2>
        <p>Enlace: <a href="{libro[4]}">{libro[4]}</a></p>
        <p>Vendedor: {libro[5]}</p>
        <hr>
        """

    contenido += "</body></html>"
 
    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    mensaje.attach(MIMEText(contenido, 'html'))

    with smtplib.SMTP(servidor_smtp, puerto) as servidor:
        servidor.starttls()
        servidor.login(usuario, contraseña)
        servidor.send_message(mensaje)


# Creo clase para cargar la tabla a la DB, ademas leer la DB y mandar el mail

class LoadTSVToPostgresOperator(BaseOperator):
    @apply_defaults
    def __init__(
            self,
            read_or_write,
            tsv_file_path,
            postgres_conn_id,
            table_name,
            *args, **kwargs):
        super(LoadTSVToPostgresOperator, self).__init__(*args, **kwargs)
        self.tsv_file_path = tsv_file_path
        self.postgres_conn_id = postgres_conn_id
        self.table_name = table_name
        self.read_or_write = read_or_write
        
    def execute(self, context):
        if self.read_or_write == "read":
            self.readDB()
        elif self.read_or_write == "write":
            self.writeDB()

    def readDB(self):
        try:
            pg_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
            connection = pg_hook.get_conn()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 10")
            
            data =[]
            for row in cursor.fetchall():
                data.append(row)
                logging.info(row)
                
            if data:                
                sendMail(data)
                
        except Exception as e:
            logging.error("Error reading data from table %s: %s", self.table_name, str(e))
            raise e
        finally:
            cursor.close()
            connection.close()
            
    def writeDB(self):
        try:
            pg_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
            connection = pg_hook.get_conn()
            with open(self.tsv_file_path, 'r', encoding="utf-8") as f:
                cursor = connection.cursor()
                cursor.copy_from(
                    file=f,
                    table=self.table_name,
                    sep='\t',
                    null='NULL'
                )
                connection.commit()
            self.log.info("Data loaded successfully into table %s", self.table_name)
        except Exception as e:
            logging.error("Error loading data into table %s: %s", self.table_name, str(e))
            raise e
        finally:
            cursor.close()
            connection.close()
