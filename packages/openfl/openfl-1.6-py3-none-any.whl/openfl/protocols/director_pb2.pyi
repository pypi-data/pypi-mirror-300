from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from openfl.protocols import base_pb2 as _base_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CudaDeviceInfo(_message.Message):
    __slots__ = ["index", "memory_total", "memory_utilized", "device_utilization", "cuda_driver_version", "cuda_version", "name"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    MEMORY_TOTAL_FIELD_NUMBER: _ClassVar[int]
    MEMORY_UTILIZED_FIELD_NUMBER: _ClassVar[int]
    DEVICE_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CUDA_DRIVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    CUDA_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    index: int
    memory_total: int
    memory_utilized: int
    device_utilization: str
    cuda_driver_version: str
    cuda_version: str
    name: str
    def __init__(self, index: _Optional[int] = ..., memory_total: _Optional[int] = ..., memory_utilized: _Optional[int] = ..., device_utilization: _Optional[str] = ..., cuda_driver_version: _Optional[str] = ..., cuda_version: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class NodeInfo(_message.Message):
    __slots__ = ["name", "cuda_devices"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUDA_DEVICES_FIELD_NUMBER: _ClassVar[int]
    name: str
    cuda_devices: _containers.RepeatedCompositeFieldContainer[CudaDeviceInfo]
    def __init__(self, name: _Optional[str] = ..., cuda_devices: _Optional[_Iterable[_Union[CudaDeviceInfo, _Mapping]]] = ...) -> None: ...

class ShardInfo(_message.Message):
    __slots__ = ["node_info", "shard_description", "n_samples", "sample_shape", "target_shape"]
    NODE_INFO_FIELD_NUMBER: _ClassVar[int]
    SHARD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    N_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SHAPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_SHAPE_FIELD_NUMBER: _ClassVar[int]
    node_info: NodeInfo
    shard_description: str
    n_samples: int
    sample_shape: _containers.RepeatedScalarFieldContainer[str]
    target_shape: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, node_info: _Optional[_Union[NodeInfo, _Mapping]] = ..., shard_description: _Optional[str] = ..., n_samples: _Optional[int] = ..., sample_shape: _Optional[_Iterable[str]] = ..., target_shape: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateShardInfoRequest(_message.Message):
    __slots__ = ["shard_info"]
    SHARD_INFO_FIELD_NUMBER: _ClassVar[int]
    shard_info: ShardInfo
    def __init__(self, shard_info: _Optional[_Union[ShardInfo, _Mapping]] = ...) -> None: ...

class UpdateShardInfoResponse(_message.Message):
    __slots__ = ["accepted"]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    accepted: bool
    def __init__(self, accepted: bool = ...) -> None: ...

class WaitExperimentRequest(_message.Message):
    __slots__ = ["collaborator_name"]
    COLLABORATOR_NAME_FIELD_NUMBER: _ClassVar[int]
    collaborator_name: str
    def __init__(self, collaborator_name: _Optional[str] = ...) -> None: ...

class WaitExperimentResponse(_message.Message):
    __slots__ = ["experiment_name"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    def __init__(self, experiment_name: _Optional[str] = ...) -> None: ...

class GetExperimentDataRequest(_message.Message):
    __slots__ = ["experiment_name", "collaborator_name"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    COLLABORATOR_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    collaborator_name: str
    def __init__(self, experiment_name: _Optional[str] = ..., collaborator_name: _Optional[str] = ...) -> None: ...

class ExperimentData(_message.Message):
    __slots__ = ["size", "npbytes"]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    NPBYTES_FIELD_NUMBER: _ClassVar[int]
    size: int
    npbytes: bytes
    def __init__(self, size: _Optional[int] = ..., npbytes: _Optional[bytes] = ...) -> None: ...

class UpdateEnvoyStatusRequest(_message.Message):
    __slots__ = ["name", "is_experiment_running", "cuda_devices"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_EXPERIMENT_RUNNING_FIELD_NUMBER: _ClassVar[int]
    CUDA_DEVICES_FIELD_NUMBER: _ClassVar[int]
    name: str
    is_experiment_running: bool
    cuda_devices: _containers.RepeatedCompositeFieldContainer[CudaDeviceInfo]
    def __init__(self, name: _Optional[str] = ..., is_experiment_running: bool = ..., cuda_devices: _Optional[_Iterable[_Union[CudaDeviceInfo, _Mapping]]] = ...) -> None: ...

class UpdateEnvoyStatusResponse(_message.Message):
    __slots__ = ["health_check_period"]
    HEALTH_CHECK_PERIOD_FIELD_NUMBER: _ClassVar[int]
    health_check_period: _duration_pb2.Duration
    def __init__(self, health_check_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class SetExperimentFailedRequest(_message.Message):
    __slots__ = ["experiment_name", "collaborator_name", "error_code", "error_description"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    COLLABORATOR_NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    collaborator_name: str
    error_code: int
    error_description: str
    def __init__(self, experiment_name: _Optional[str] = ..., collaborator_name: _Optional[str] = ..., error_code: _Optional[int] = ..., error_description: _Optional[str] = ...) -> None: ...

class SetExperimentFailedResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetExperimentsListRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExperimentListItem(_message.Message):
    __slots__ = ["name", "status", "collaborators_amount", "tasks_amount", "progress"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COLLABORATORS_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TASKS_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: str
    collaborators_amount: int
    tasks_amount: int
    progress: float
    def __init__(self, name: _Optional[str] = ..., status: _Optional[str] = ..., collaborators_amount: _Optional[int] = ..., tasks_amount: _Optional[int] = ..., progress: _Optional[float] = ...) -> None: ...

class GetExperimentsListResponse(_message.Message):
    __slots__ = ["experiments"]
    EXPERIMENTS_FIELD_NUMBER: _ClassVar[int]
    experiments: _containers.RepeatedCompositeFieldContainer[ExperimentListItem]
    def __init__(self, experiments: _Optional[_Iterable[_Union[ExperimentListItem, _Mapping]]] = ...) -> None: ...

class GetExperimentDescriptionRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetExperimentDescriptionResponse(_message.Message):
    __slots__ = ["experiment"]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    experiment: _base_pb2.ExperimentDescription
    def __init__(self, experiment: _Optional[_Union[_base_pb2.ExperimentDescription, _Mapping]] = ...) -> None: ...

class ExperimentInfo(_message.Message):
    __slots__ = ["name", "collaborator_names", "experiment_data", "model_proto"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLLABORATOR_NAMES_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_DATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_PROTO_FIELD_NUMBER: _ClassVar[int]
    name: str
    collaborator_names: _containers.RepeatedScalarFieldContainer[str]
    experiment_data: ExperimentData
    model_proto: _base_pb2.ModelProto
    def __init__(self, name: _Optional[str] = ..., collaborator_names: _Optional[_Iterable[str]] = ..., experiment_data: _Optional[_Union[ExperimentData, _Mapping]] = ..., model_proto: _Optional[_Union[_base_pb2.ModelProto, _Mapping]] = ...) -> None: ...

class SetNewExperimentResponse(_message.Message):
    __slots__ = ["accepted"]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    accepted: bool
    def __init__(self, accepted: bool = ...) -> None: ...

class GetExperimentStatusRequest(_message.Message):
    __slots__ = ["experiment_name"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    def __init__(self, experiment_name: _Optional[str] = ...) -> None: ...

class GetExperimentStatusResponse(_message.Message):
    __slots__ = ["experiment_status"]
    EXPERIMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    experiment_status: str
    def __init__(self, experiment_status: _Optional[str] = ...) -> None: ...

class GetTrainedModelRequest(_message.Message):
    __slots__ = ["experiment_name", "model_type"]
    class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        BEST_MODEL: _ClassVar[GetTrainedModelRequest.ModelType]
        LAST_MODEL: _ClassVar[GetTrainedModelRequest.ModelType]
    BEST_MODEL: GetTrainedModelRequest.ModelType
    LAST_MODEL: GetTrainedModelRequest.ModelType
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    model_type: GetTrainedModelRequest.ModelType
    def __init__(self, experiment_name: _Optional[str] = ..., model_type: _Optional[_Union[GetTrainedModelRequest.ModelType, str]] = ...) -> None: ...

class TrainedModelResponse(_message.Message):
    __slots__ = ["model_proto"]
    MODEL_PROTO_FIELD_NUMBER: _ClassVar[int]
    model_proto: _base_pb2.ModelProto
    def __init__(self, model_proto: _Optional[_Union[_base_pb2.ModelProto, _Mapping]] = ...) -> None: ...

class GetDatasetInfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDatasetInfoResponse(_message.Message):
    __slots__ = ["shard_info"]
    SHARD_INFO_FIELD_NUMBER: _ClassVar[int]
    shard_info: ShardInfo
    def __init__(self, shard_info: _Optional[_Union[ShardInfo, _Mapping]] = ...) -> None: ...

class GetMetricStreamRequest(_message.Message):
    __slots__ = ["experiment_name"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    def __init__(self, experiment_name: _Optional[str] = ...) -> None: ...

class GetMetricStreamResponse(_message.Message):
    __slots__ = ["metric_origin", "task_name", "metric_name", "metric_value", "round"]
    METRIC_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    metric_origin: str
    task_name: str
    metric_name: str
    metric_value: float
    round: int
    def __init__(self, metric_origin: _Optional[str] = ..., task_name: _Optional[str] = ..., metric_name: _Optional[str] = ..., metric_value: _Optional[float] = ..., round: _Optional[int] = ...) -> None: ...

class RemoveExperimentRequest(_message.Message):
    __slots__ = ["experiment_name"]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    def __init__(self, experiment_name: _Optional[str] = ...) -> None: ...

class RemoveExperimentResponse(_message.Message):
    __slots__ = ["acknowledgement"]
    ACKNOWLEDGEMENT_FIELD_NUMBER: _ClassVar[int]
    acknowledgement: bool
    def __init__(self, acknowledgement: bool = ...) -> None: ...

class EnvoyInfo(_message.Message):
    __slots__ = ["shard_info", "is_online", "is_experiment_running", "last_updated", "valid_duration", "experiment_name"]
    SHARD_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_ONLINE_FIELD_NUMBER: _ClassVar[int]
    IS_EXPERIMENT_RUNNING_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    VALID_DURATION_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    shard_info: ShardInfo
    is_online: bool
    is_experiment_running: bool
    last_updated: _timestamp_pb2.Timestamp
    valid_duration: _duration_pb2.Duration
    experiment_name: str
    def __init__(self, shard_info: _Optional[_Union[ShardInfo, _Mapping]] = ..., is_online: bool = ..., is_experiment_running: bool = ..., last_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., valid_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., experiment_name: _Optional[str] = ...) -> None: ...

class GetEnvoysRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetEnvoysResponse(_message.Message):
    __slots__ = ["envoy_infos"]
    ENVOY_INFOS_FIELD_NUMBER: _ClassVar[int]
    envoy_infos: _containers.RepeatedCompositeFieldContainer[EnvoyInfo]
    def __init__(self, envoy_infos: _Optional[_Iterable[_Union[EnvoyInfo, _Mapping]]] = ...) -> None: ...
