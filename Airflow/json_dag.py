import requests
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator




default_args = {
    "owner": "Owner Name",
    "depends_on_past": False,
    "start_date": datetime(2023,1, 1),
    # "email_on_failure": True,
    # "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}
#To get all the requests of an API you may need to work with pagination, where you iterate the results 
#based on the number of total pages. In other words, you need the total pages first
def get_api_pagination(**context):

    TOKEN = Variable.get("api_access_token")  
    #You will net a token to access the API. Save it as a variable in Airflow UI
    header = {
        "PRIVATE-TOKEN": TOKEN
    }   
    params = {
        "scope": "all",
        "page": "1", 
        "per_page": "20"
    }
    #The params depend on the API documentation   
    url = "the API url"

    data_head = requests.head(url=url, headers=header)
    dict_response = dict(data_head.headers)["X-Total-Pages"]
    #Check how the "Total-Pages" is called in your API request
    total_page = int(dict_response)
    return total_page


def get_data(**context):
    
    ti = context["ti"]
    total_page = ti.xcom_pull(task_ids="get_api_pagination")

    TOKEN = Variable.get("api_access_token")

    temp_dict = {'col_1':[],'col_2':[], 'col_3':[]}
    
    header = {
        "PRIVATE-TOKEN": TOKEN
    }   
    params = {
        "scope": "all",
        "page": "1", 
        "per_page": "20"
    }   
    url = "the API url"


    print('Starting append process')

    for page in range(1,total_page+1):
        params["page"] = page
        response = requests.get(url, params=params, headers=header).json()
        for issue in response:
            temp_dict['json_col_1'].append(issue['col_1'])
            temp_dict['json_col_2'].append(issue['col_2'])
            temp_dict['json_col_3'].append(issue['col_3'])
            # You append the the json file's value in your columns
    print('Appending proccess completed')
    df = pd.DataFrame(data=temp_dict)
    file_time = datetime.datetime.now().strftime("%Y-%m-%d")
    csv_df = df.to_csv(f'set/the/path/and/file_name-{file_time}.csv')
    return print("Csv should be inside the folder now")

dag = DAG(
    "DAG_Name",
    default_args=default_args,
    catchup=True,
    schedule_interval='@daily',
    max_active_runs=1
)

start_dag = DummyOperator(
    task_id='start_dag',
    dag=dag
)

get_api_pagination = PythonOperator(
    task_id="get_api_pagination",
    python_callable=get_api_pagination,
    provide_context=True,
    dag=dag,
)

get_data = PythonOperator(
    task_id="get_data",
    python_callable=get_data,
    provide_context=True,
    dag=dag,
)

end_dag = DummyOperator(
    task_id='end_dag',
    dag=dag
)


start_dag >> get_api_pagination >> get_data >> end_dag