from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1274() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Sample", None, Sample, ROCrateObject_reflection())


class Sample(ROCrateObject):
    def __init__(self, id: str, name: Any=None, additional_type: str | None=None, additional_property: Any | None=None, derives_from: Any | None=None) -> None:
        super().__init__(id, "bioschemas.org/Sample", additional_type)
        this: FSharpRef[Sample] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_optional_property("additionalProperty", additional_property, this.contents)
        set_optional_property("derivesFrom", derives_from, this.contents)


Sample_reflection = _expr1274

def Sample__ctor_7AC741F8(id: str, name: Any=None, additional_type: str | None=None, additional_property: Any | None=None, derives_from: Any | None=None) -> Sample:
    return Sample(id, name, additional_type, additional_property, derives_from)


__all__ = ["Sample_reflection"]

