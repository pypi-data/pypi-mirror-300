from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

ADDITION: Operation
DESCRIPTOR: _descriptor.FileDescriptor
DIVISION: Operation
MULTIPLICATION: Operation
OPERATION_UNSPECIFIED: Operation
SUBTRACTION: Operation

class CalculationNode(_message.Message):
    __slots__ = ["column_dtype", "operands", "operation"]
    COLUMN_DTYPE_FIELD_NUMBER: ClassVar[int]
    OPERANDS_FIELD_NUMBER: ClassVar[int]
    OPERATION_FIELD_NUMBER: ClassVar[int]
    column_dtype: _data_type__client_pb2.DataType
    operands: _containers.RepeatedCompositeFieldContainer[Operand]
    operation: Operation
    def __init__(self, operation: Optional[Union[Operation, str]] = ..., operands: Optional[Iterable[Union[Operand, Mapping]]] = ..., column_dtype: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ...) -> None: ...

class LiteralValueType(_message.Message):
    __slots__ = ["bool_value", "float32_value", "float64_value", "int64_value", "null_value", "string_value"]
    BOOL_VALUE_FIELD_NUMBER: ClassVar[int]
    FLOAT32_VALUE_FIELD_NUMBER: ClassVar[int]
    FLOAT64_VALUE_FIELD_NUMBER: ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: ClassVar[int]
    NULL_VALUE_FIELD_NUMBER: ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: ClassVar[int]
    bool_value: bool
    float32_value: float
    float64_value: float
    int64_value: int
    null_value: NullLiteralValue
    string_value: str
    def __init__(self, float32_value: Optional[float] = ..., float64_value: Optional[float] = ..., int64_value: Optional[int] = ..., bool_value: bool = ..., string_value: Optional[str] = ..., null_value: Optional[Union[NullLiteralValue, Mapping]] = ...) -> None: ...

class NullLiteralValue(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Operand(_message.Message):
    __slots__ = ["calculation_node", "input_feature_name", "literal_value"]
    CALCULATION_NODE_FIELD_NUMBER: ClassVar[int]
    INPUT_FEATURE_NAME_FIELD_NUMBER: ClassVar[int]
    LITERAL_VALUE_FIELD_NUMBER: ClassVar[int]
    calculation_node: CalculationNode
    input_feature_name: str
    literal_value: LiteralValueType
    def __init__(self, input_feature_name: Optional[str] = ..., calculation_node: Optional[Union[CalculationNode, Mapping]] = ..., literal_value: Optional[Union[LiteralValueType, Mapping]] = ...) -> None: ...

class Operation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
