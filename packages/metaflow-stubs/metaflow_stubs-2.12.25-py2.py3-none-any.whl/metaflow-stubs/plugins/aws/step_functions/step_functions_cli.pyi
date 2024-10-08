##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.25                                                            #
# Generated on 2024-10-07T19:08:03.902390                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.metaflow_current
    import metaflow.decorators
    import metaflow.parameters
    import metaflow.exception

JSONType: metaflow.parameters.JSONTypeClass

current: metaflow.metaflow_current.Current

def get_metadata() -> str:
    """
    Returns the current Metadata provider.
    
    If this is not set explicitly using `metadata`, the default value is
    determined through the Metaflow configuration. You can use this call to
    check that your configuration is set up properly.
    
    If multiple configuration profiles are present, this call returns the one
    selected through the `METAFLOW_PROFILE` environment variable.
    
    Returns
    -------
    str
        Information about the Metadata provider currently selected. This information typically
        returns provider specific information (like URL for remote providers or local paths for
        local providers).
    """
    ...

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

SERVICE_VERSION_CHECK: bool

SFN_STATE_MACHINE_PREFIX: None

UI_URL: None

class BatchDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies that this step should execute on [AWS Batch](https://aws.amazon.com/batch/).
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    gpu : int, default 0
        Number of GPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on AWS Batch. If not specified, and
        METAFLOW_BATCH_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    queue : str, default METAFLOW_BATCH_JOB_QUEUE
        AWS Batch Job Queue to submit the job to.
    iam_role : str, default METAFLOW_ECS_S3_ACCESS_IAM_ROLE
        AWS IAM role that AWS Batch container uses to access AWS cloud resources.
    execution_role : str, default METAFLOW_ECS_FARGATE_EXECUTION_ROLE
        AWS IAM role that AWS Batch can use [to trigger AWS Fargate tasks]
        (https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html).
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    max_swap : int, optional, default None
        The total amount of swap memory (in MiB) a container can use for this
        step. This parameter is translated to the `--memory-swap` option in
        Docker where the value is the sum of the container memory plus the
        `max_swap` value.
    swappiness : int, optional, default None
        This allows you to tune memory swappiness behavior for this step.
        A swappiness value of 0 causes swapping not to happen unless absolutely
        necessary. A swappiness value of 100 causes pages to be swapped very
        aggressively. Accepted values are whole numbers between 0 and 100.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step. Note that tmpfs is
        not available on Fargate compute environments
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default None
        Path to tmpfs mount for this step. Defaults to /metaflow_temp.
    inferentia : int, default 0
        Number of Inferentia chips required for this step.
    trainium : int, default None
        Alias for inferentia. Use only one of the two.
    efa : int, default 0
        Number of elastic fabric adapter network devices to attach to container
    ephemeral_storage : int, default None
        The total amount, in GiB, of ephemeral storage to set for the task, 21-200GiB.
        This is only relevant for Fargate compute environments
    log_driver: str, optional, default None
        The log driver to use for the Amazon ECS container.
    log_options: List[str], optional, default None
        List of strings containing options for the chosen log driver. The configurable values
        depend on the `log driver` chosen. Validation of these options is not supported yet.
        Example: [`awslogs-group:aws/batch/job`]
    """
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
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

def validate_tags(tags, existing_tags = None):
    """
    Raises MetaflowTaggingError if invalid based on these rules:
    
    Tag set size is too large. But it's OK if tag set is not larger
    than an existing tag set (if provided).
    
    Then, we validate each tag.  See validate_tag()
    """
    ...

def load_token(token_prefix):
    ...

def new_token(token_prefix, prev_token = None):
    ...

def store_token(token_prefix, token):
    ...

class StepFunctions(object, metaclass=type):
    def __init__(self, name, graph, flow, code_package_sha, code_package_url, production_token, metadata, flow_datastore, environment, event_logger, monitor, tags = None, namespace = None, username = None, max_workers = None, workflow_timeout = None, is_project = False, use_distributed_map = False):
        ...
    def to_json(self):
        ...
    def trigger_explanation(self):
        ...
    def deploy(self, log_execution_history):
        ...
    def schedule(self):
        ...
    @classmethod
    def delete(cls, name):
        ...
    @classmethod
    def terminate(cls, flow_name, name):
        ...
    @classmethod
    def trigger(cls, name, parameters):
        ...
    @classmethod
    def list(cls, name, states):
        ...
    @classmethod
    def get_existing_deployment(cls, name):
        ...
    @classmethod
    def get_execution(cls, state_machine_name, name):
        ...
    ...

class IncorrectProductionToken(metaflow.exception.MetaflowException, metaclass=type):
    ...

class RunIdMismatch(metaflow.exception.MetaflowException, metaclass=type):
    ...

class IncorrectMetadataServiceVersion(metaflow.exception.MetaflowException, metaclass=type):
    ...

class StepFunctionsStateMachineNameTooLong(metaflow.exception.MetaflowException, metaclass=type):
    ...

def check_metadata_service_version(obj):
    ...

def resolve_state_machine_name(obj, name):
    ...

def make_flow(obj, token, name, tags, namespace, max_workers, workflow_timeout, is_project, use_distributed_map):
    ...

def resolve_token(name, token_prefix, obj, authorize, given_token, generate_new_token, is_project):
    ...

def validate_run_id(state_machine_name, token_prefix, authorize, run_id, instructions_fn = None):
    ...

def validate_token(name, token_prefix, authorize, instruction_fn = None):
    """
    Validate that the production token matches that of the deployed flow.
    
    In case both the user and token do not match, raises an error.
    Optionally outputs instructions on token usage via the provided instruction_fn(flow_name, prev_user)
    """
    ...

