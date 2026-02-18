from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

class OperationType(Enum):
    MODULE = "module"
    PIPX = "pipx"

@dataclass
class OperationBase:
    name: str

@dataclass
class Operation(OperationBase):
    operation_type: OperationType
    operation_module: str | None = None

@dataclass
class OperationFolder(OperationBase):
    portfolio: list[Operation | OperationFolder] = field(default_factory=list)


class ParameterType(Enum):
    PREFERENCE = "preference"
    STRING_VALUE = "string_value"
    VALUE_OPTIONS = "value_options"
    PARAMETER_LIST = "parameter_list"
    PARAMETER_OPTIONS_TO_LIST = "parameter_options_to_list"

@dataclass
class ParameterBase:
    type: ParameterType = field(init=False)
    name: str
    mandatory: bool = False
    description: str | None = None
    isSelected: bool = False

    def __post_init__(self):
       if self.mandatory:
          self.isSelected = True

@dataclass
class ParameterPreference(ParameterBase):
    def __post_init__(self):
      super().__post_init__()
      self.type = ParameterType.PREFERENCE

@dataclass
class ParameterStringValue(ParameterBase):
    value: str = ''

    def __post_init__(self):
      super().__post_init__()
      self.type = ParameterType.STRING_VALUE

@dataclass
class ParameterList(ParameterBase):
    parameters: list[ParameterBase] = field(default_factory=list)

    def __post_init__(self):
      super().__post_init__()
      self.type = ParameterType.PARAMETER_LIST


@dataclass
class ParameterOptionsToList(ParameterBase):
    options: list[ParameterList] = field(default_factory=list)
    selectedListIdx: int = -1

    def __post_init__(self):
      super().__post_init__()
      self.type = ParameterType.PARAMETER_OPTIONS_TO_LIST

ParameterData = ParameterList | ParameterOptionsToList


class LibraryAPI(ABC):
    @abstractmethod
    def getOperationHierarchy(self) -> OperationFolder:
        pass

    @abstractmethod
    def getDescription(self, operationBranch: list[str]) -> str:
        pass

    @abstractmethod
    def getParameters(self, operationBranch: list[str]) -> ParameterData:
        pass

    @abstractmethod
    def submitOperation(self, operationBranch: list[str], command: list[str], servers: list[str]) -> dict:
        pass
