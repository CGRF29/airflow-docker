from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.filesystem import FileSensor
from generate_platzi_data import _generate_platzi_data
from datetime import datetime, date

default_args={"depends_on_past":True}

with DAG(dag_id="Proyecto_SpaceX_v1",
         description="Proyecto Platzi explora el espacio",
         schedule_interval="@daily",
         start_date=datetime(2024,3,1),
         end_date=datetime(2024,4,1),
         max_active_runs=1) as dag:
    
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
    
    t7 = BashOperator(task_id="Enviar_Mensaje",
                      bash_command="echo '{{ds}}: Los datos fueron cargados'")
    
    t1 >>  t2 >> t3 >> t4 >> t5 >> t6 >> t7
    
