##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25                                                            #
# Generated on 2024-10-07T19:08:03.874244                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.decorators
    import metaflow.metaflow_current

current: metaflow.metaflow_current.Current

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

def load_token(token_prefix):
    ...

def new_token(token_prefix, prev_token = None):
    ...

def store_token(token_prefix, token):
    ...

class KubernetesDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies that this step should execute on Kubernetes.
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    disk : int, default 10240
        Disk size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on Kubernetes. If not specified, and
        METAFLOW_KUBERNETES_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    image_pull_policy: str, default KUBERNETES_IMAGE_PULL_POLICY
        If given, the imagePullPolicy to be applied to the Docker image of the step.
    service_account : str, default METAFLOW_KUBERNETES_SERVICE_ACCOUNT
        Kubernetes service account to use when launching pod in Kubernetes.
    secrets : List[str], optional, default None
        Kubernetes secrets to use when launching pod in Kubernetes. These
        secrets are in addition to the ones defined in `METAFLOW_KUBERNETES_SECRETS`
        in Metaflow configuration.
    node_selector: Union[Dict[str,str], str], optional, default None
        Kubernetes node selector(s) to apply to the pod running the task.
        Can be passed in as a comma separated string of values e.g. "kubernetes.io/os=linux,kubernetes.io/arch=amd64"
        or as a dictionary {"kubernetes.io/os": "linux", "kubernetes.io/arch": "amd64"}
    namespace : str, default METAFLOW_KUBERNETES_NAMESPACE
        Kubernetes namespace to use when launching pod in Kubernetes.
    gpu : int, optional, default None
        Number of GPUs required for this step. A value of zero implies that
        the scheduled node should not have GPUs.
    gpu_vendor : str, default KUBERNETES_GPU_VENDOR
        The vendor of the GPUs to be used for this step.
    tolerations : List[str], default []
        The default is extracted from METAFLOW_KUBERNETES_TOLERATIONS.
        Kubernetes tolerations to use when launching pod in Kubernetes.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step.
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default: None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default /metaflow_temp
        Path to tmpfs mount for this step.
    persistent_volume_claims : Dict[str, str], optional, default None
        A map (dictionary) of persistent volumes to be mounted to the pod for this step. The map is from persistent
        volumes to the path to which the volume is to be mounted, e.g., `{'pvc-name': '/path/to/mount/on'}`.
    shared_memory: int, optional
        Shared memory size (in MiB) required for this step
    port: int, optional
        Port number to specify in the Kubernetes job object
    compute_pool : str, optional, default None
        Compute pool to be used for for this step.
        If not specified, any accessible compute pool within the perimeter is used.
    """
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def package_init(self, flow, step_name, environment):
        ...
    def runtime_init(self, flow, graph, package, run_id):
        ...
    def runtime_task_created(self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context):
        ...
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow, graph, is_task_ok, retry_count, max_retries):
        ...
    ...

class Airflow(object, metaclass=type):
    def __init__(self, name, graph, flow, code_package_sha, code_package_url, metadata, flow_datastore, environment, event_logger, monitor, production_token, tags = None, namespace = None, username = None, max_workers = None, worker_pool = None, description = None, file_path = None, workflow_timeout = None, is_paused_upon_creation = True):
        ...
    @classmethod
    def get_existing_deployment(cls, name, flow_datastore):
        ...
    @classmethod
    def get_token_path(cls, name):
        ...
    @classmethod
    def save_deployment_token(cls, owner, name, token, flow_datastore):
        ...
    def compile(self):
        ...
    ...

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def make_flow(obj, dag_name, production_token, tags, is_paused_upon_creation, namespace, max_workers, workflow_timeout, worker_pool, file):
    ...

def resolve_dag_name(name):
    ...

