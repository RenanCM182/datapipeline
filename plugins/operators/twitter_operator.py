from airflow import DAG
from airflow.models import BaseOperator, DagModel, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.twitter_hook import TwitterHook
import json
from datetime import datetime

class TwitterOperator(BaseOperator):


    @apply_defaults
    def __init__(
        self,
        query,
        conn_id = None,
        start_time = None,
        end_time = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.query = query
        self.conn_id = conn_id
        self.start_time = start_time
        self.end_time = end_time


    def execute (self, context):
        hook = TwitterHook(
            query = self.query,
            conn_id = self.conn_id,
            start_time = self.start_time,
            end_time = self.end_time
        )
        for pg in hook.run():
            print(json.dumps(pg, indent=4, sort_keys=True))

if __name__ == "__main__":

    # criando dag para teste, para que assim seja possível executar o operator
    with DAG(dag_id="TwitterTest", start_date=datetime.now()) as dag:

        to = TwitterOperator(query="AluraOline", task_id="test_run")

        # todos funcionaram, aparentemente tudo redundante, preciso entender melhor esse etapa.
        # ti = TaskInstance(task=to, run_id=to.task_id)
        # ti = TaskInstance(task=to, run_id=dag.dag_id)
        ti = TaskInstance(task=to)

        # também funcionou passando o próprio id da task to.execute(to.task_id)
        to.execute(ti.task_id)