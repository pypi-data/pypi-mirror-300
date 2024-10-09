from __future__ import annotations
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1253() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Dataset", None, Dataset, ROCrateObject_reflection())


class Dataset(ROCrateObject):
    def __init__(self, id: str, additional_type: str | None=None) -> None:
        super().__init__(id, "schema.org/Dataset", additional_type)
        pass


Dataset_reflection = _expr1253

def Dataset__ctor_27AED5E3(id: str, additional_type: str | None=None) -> Dataset:
    return Dataset(id, additional_type)


__all__ = ["Dataset_reflection"]

