"""
Proyecto: Platzi explora el espacio

"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, date
from generate_platzi_data import _generate_platzi_data
from airflow.operators.email import EmailOperator

default_args = {
    'start_date': datetime(2024, 1, 1),
    'end_date': datetime(2024, 3, 1)
}
# Contraseña: ttqt tbuz dgyc fkfq

with DAG(dag_id='Proyecto_SpaceX',
         description='Pipeline for collecting Platzi and SpaceX data',
         schedule_interval='@monthly',
         default_args=default_args,
         max_active_runs=1) as dag:
    
    #Esperar a que la NASA nos dé autorización para acceder a los datos del satélite.
    #Enviar un mensaje a los equipos de que los datos finales están disponibles
    t1 = BashOperator(task_id="Confirmacion_NASA",
                      bash_command="sleep 20 && echo 'Confirmación, puede proceder' > /tmp/response_{{ ds_nodash }}.txt",
                      retries=2,
                      retry_delay=5)
    
    t2 = BashOperator(task_id="Lectura_Datos_NASA",
                      bash_command="ls /tmp && head /tmp/response_{{ds_nodash}}.txt")
    
    t3 = BashOperator(task_id="Obtener_datos_SpaceX",
                                bash_command="curl -o /tmp/history.json -L 'https://api.spacexdata.com/v4/history'")
    
    t4 = PythonOperator(task_id="Respuesta_Satelite",
                        python_callable=_generate_platzi_data)
    
    t5 = FileSensor(task_id="Esperar_archivo",
                    filepath="/tmp/platzi_data_{{ds_nodash}}.csv")
    
    t6 = BashOperator(task_id="Visualizar_Respuesta_Satelite",
                      bash_command="ls /tmp && head /tmp/platzi_data_{{ds_nodash}}.csv")


    email_equipo = EmailOperator(task_id='Notificar_Equipo',
                                conn_id='smtp_default',
                                to = "gaby96.flores@gmail.com",
                                subject = "Notificación Datos finales disponibles",
                                html_content = "Los datos finales están disponibles",
                                dag = dag)                 

    t1 >> t2 >> [t3, t4] >> t5 >> t6 >> email_equipo
