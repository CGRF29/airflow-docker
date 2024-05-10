"""
Dependencias entre tareas

#Opcion 1:
tarea1.set_downstream(tarea2)
tarea2.set_downstream(tarea3)

#Opción 2: bitshift operators
tarea1 >> tarea 2 >> tarea 3

Ejecucción de dos tareas en paralelo

#Opcion 1:
tarea1.set_downstream([tarea2,tarea3])
#Opción 2:
tarea1 >> [tarea2,tarea3]
#Opción extra:
tarea1.set_upstream([tarea2,tarea3])
tarea1 << [tarea2, tarea3]
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

def print_hello():
    print("Hello gente de Platzi")

with DAG(dag_id="dependencias",
         description="Nuestro primer DAG creando dependencias entre tareas",
         schedule_interval="@once",
         start_date=datetime(2024,5,7)) as dag:
    
    t1 = PythonOperator(task_id="tarea1",
                        python_callable=print_hello) 
    t2 = BashOperator(task_id="tarea2",
                      bash_command="echo 'tarea 2'")
    t3 = BashOperator(task_id="tarea3",
                      bash_command="echo 'tarea 3'")
    t4 = BashOperator(task_id="tarea4",
                      bash_command="echo 'tarea 4'")
    #Opcion 1
    #t1.set_downstream(t2)
    #t2.set_downstream([t3,t4])
    
    #Opcion 2
    t1 >> t2 >> [t3,t4]