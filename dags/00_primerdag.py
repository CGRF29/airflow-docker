"""
Primer DAG

Elementos:
dag_id: Nombre unico
descricption: Breve descripción
start_date: Día en que comenzará la ejecucción
schedule_interval: Número de veces en que se ejecutará
t1 : Esto se llama el dependency tasks que es la manera en la cual 
creamos el graph. Esto significa que aquí decimos el orden de las tareas.
"""
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(dag_id="primerdag", 
         description="Nuestro primer DAG", 
         start_date=datetime(2024,5,7),
         schedule_interval="@once") as dag:
   t1 = EmptyOperator(task_id="dummy")
   t1 