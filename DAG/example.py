from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod as kubernetes_pod_operator

namespace = "example_space"
ENV = "dev"
DOCKER_REGISTRY_SERVER = "example"
REPOSITORY_PATH = "example/example"
GCS_IMG = DOCKER_REGISTRY_SERVER + REPOSITORY_PATH + "/azure_utils:" + ENV


GCS_SCRIPT_PATH = "./list_buckets.py"

annotations = {
    "vault.hashicorp.com/agent-inject": "true",
    "vault.hashicorp.com/agent-pre-populate-only": "true",
    "vault.hashicorp.com/role": namespace,

    "vault.hashicorp.com/agent-inject-secret-sfmc_sftp_ap.json": "secret/example",
    "vault.hashicorp.com/agent-inject-template-sfmc_sftp_ap.json": '''{{ with secret "secret/data/teams/gdo-analytics/sfmc_sftp/sfmc_sftp_ap"}}
    {{ .Data.data | toJSON }}
    {{ end }}''',
    "vault.hashicorp.com/agent-inject-secret-gcp-sa-storage.json": "secret/data/gcp-service-accounts/cp-gdo-dev-analytics/gcp-sa-storage",
    "vault.hashicorp.com/agent-inject-template-gcp-sa-storage.json": '''{{ with secret "secret/data/gcp-service-accounts/cp-gdo-dev-analytics/gcp-sa-storage"}}
        {{ .Data.data | toJSON }}
        {{ end }}''',

    "vault.hashicorp.com/tls-skip-verify": "true",
}

args = {
    "owner": "SDG",
    # API container has 3 day lag from scheduler, so start on 4th January
    "start_date": datetime(2021, 12, 8),
    "email": ["example@sdggroup.com"],
    "email_on_failure": True,
    "retries": 0,
    "retry_delay": timedelta(minutes=10),
    "startup_timeout_seconds": 90,
}

with DAG(dag_id='gcs_poc_dag', schedule_interval=None, start_date=datetime(2021, 12, 9), catchup=False,
         default_args=args) as dag:
    start_task = DummyOperator(task_id='start')

    get_file_from_sftp_task = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="ex_poc_task",
        name="ex_poc_task",
        namespace=namespace,
        image=GCS_IMG,
        image_pull_policy="Always",
        cmds=["python", GCS_SCRIPT_PATH],
        annotations=annotations,
        get_logs=True,
        is_delete_operator_pod=True,
        service_account_name="vault-sidecar",
    )

    end_task = DummyOperator(task_id='end')

    start_task >> get_file_from_sftp_task >> end_task
