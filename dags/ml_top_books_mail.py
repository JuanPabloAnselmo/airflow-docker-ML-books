from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
from operators.Load_table_to_postgres import LoadTSVToPostgresOperator

default_args = {
    'owner': 'jpanselmo',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG (
    
    dag_id= "dag_ml_top_books_mail",
    default_args=default_args,
    start_date= datetime(2024, 4, 3, 11, 30),
    schedule_interval="@weekly"
    
) as dag:
    
    t1 = PostgresOperator(
        task_id="create_table",
        postgres_conn_id = "postgres_localhost",
        sql= """
        CREATE TABLE IF NOT EXISTS libros_most_relevant (
            id VARCHAR(30),
            title VARCHAR(500),
            price VARCHAR(50),
            thumbnail VARCHAR(500),
            permalink VARCHAR(500),
            seller VARCHAR(200),
            created_date VARCHAR(15)
            
        )
        """
    )    
    
    t2= BashOperator(
        task_id="consult_api",             
        bash_command= "python /opt/airflow/dags/api_consult.py"
    )
    

    
    t3 = LoadTSVToPostgresOperator(
            task_id='write_table',
            read_or_write="write",
            tsv_file_path='/opt/airflow/dags/data/items.tsv',
            postgres_conn_id='postgres_localhost',
            table_name='libros_most_relevant'
        
    )
    
    t4 = LoadTSVToPostgresOperator(
            task_id='read_table_and_send_mail',
            read_or_write="read",
            tsv_file_path='/opt/airflow/dags/data/items.tsv',
            postgres_conn_id='postgres_localhost',
            table_name='libros_most_relevant'
        
    )
    
    t1 >> t2 >> t3 >> t4