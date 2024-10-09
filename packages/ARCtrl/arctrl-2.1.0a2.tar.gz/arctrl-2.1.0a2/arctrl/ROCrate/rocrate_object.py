from __future__ import annotations
from abc import abstractmethod
from typing import Protocol
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)

class IROCrateObject(Protocol):
    @property
    @abstractmethod
    def AdditionalType(self) -> str | None:
        ...

    @AdditionalType.setter
    @abstractmethod
    def AdditionalType(self, __arg0: str | None) -> None:
        ...

    @property
    @abstractmethod
    def Id(self) -> str:
        ...

    @property
    @abstractmethod
    def SchemaType(self) -> str:
        ...

    @SchemaType.setter
    @abstractmethod
    def SchemaType(self, __arg0: str) -> None:
        ...


def _expr1252() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.ROCrateObject", None, ROCrateObject, DynamicObj_reflection())


class ROCrateObject(DynamicObj):
    def __init__(self, id: str, schema_type: str, additional_type: str | None=None) -> None:
        super().__init__()
        self.id: str = id
        self._schemaType: str = schema_type
        self._additionalType: str | None = additional_type

    @property
    def SchemaType(self, __unit: None=None) -> str:
        this: ROCrateObject = self
        return this._schemaType

    @SchemaType.setter
    def SchemaType(self, value: str) -> None:
        this: ROCrateObject = self
        this._schemaType = value

    @property
    def Id(self, __unit: None=None) -> str:
        this: ROCrateObject = self
        return this.id

    @property
    def AdditionalType(self, __unit: None=None) -> str | None:
        this: ROCrateObject = self
        return this._additionalType

    @AdditionalType.setter
    def AdditionalType(self, value: str | None=None) -> None:
        this: ROCrateObject = self
        this._additionalType = value


ROCrateObject_reflection = _expr1252

def ROCrateObject__ctor_Z2FC25A28(id: str, schema_type: str, additional_type: str | None=None) -> ROCrateObject:
    return ROCrateObject(id, schema_type, additional_type)


def ROCrateObject__get_Id(this: ROCrateObject) -> str:
    return this.id


def ROCrateObject__get_SchemaType(this: ROCrateObject) -> str:
    return this._schemaType


def ROCrateObject__set_SchemaType_Z721C83C5(this: ROCrateObject, value: str) -> None:
    this._schemaType = value


def ROCrateObject__get_AdditionalType(this: ROCrateObject) -> str | None:
    return this._additionalType


def ROCrateObject__set_AdditionalType_6DFDD678(this: ROCrateObject, value: str | None=None) -> None:
    this._additionalType = value


__all__ = ["ROCrateObject_reflection", "ROCrateObject__get_Id", "ROCrateObject__get_SchemaType", "ROCrateObject__set_SchemaType_Z721C83C5", "ROCrateObject__get_AdditionalType", "ROCrateObject__set_AdditionalType_6DFDD678"]

