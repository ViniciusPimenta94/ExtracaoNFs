from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from faturas_para_extrair_nf import main as extrair_faturas_nf

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='extracao_nf_gpt',
    default_args=default_args,
    schedule_interval='0 8 */1 * 1-5',
    catchup=False,
    tags=['notas_fiscais', 'openai', 'twm'],
    description='Extrai notas fiscais de faturas e envia para o TWM usando OpenAI',
) as dag:

    tarefa_extrair_nf = PythonOperator(
        task_id='executar_extracao_faturas',
        python_callable=extrair_faturas_nf
    )
