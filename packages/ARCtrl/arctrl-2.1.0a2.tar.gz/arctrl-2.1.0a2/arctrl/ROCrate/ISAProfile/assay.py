from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from .dataset import (Dataset, Dataset_reflection)

def _expr1256() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Assay", None, Assay, Dataset_reflection())


class Assay(Dataset):
    def __init__(self, id: str, identifier: Any=None, about: Any | None=None, comment: Any | None=None, creator: Any | None=None, has_part: Any | None=None, measurement_method: Any | None=None, measurement_technique: Any | None=None, url: Any | None=None, variable_measured: Any | None=None) -> None:
        super().__init__(id, "Assay")
        this: FSharpRef[Assay] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("identifier", identifier, this.contents)
        set_optional_property("measurementMethod", measurement_method, this.contents)
        set_optional_property("measurementTechnique", measurement_technique, this.contents)
        set_optional_property("variableMeasured", variable_measured, this.contents)
        set_optional_property("about", about, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("creator", creator, this.contents)
        set_optional_property("hasPart", has_part, this.contents)
        set_optional_property("url", url, this.contents)


Assay_reflection = _expr1256

def Assay__ctor_28BFDC80(id: str, identifier: Any=None, about: Any | None=None, comment: Any | None=None, creator: Any | None=None, has_part: Any | None=None, measurement_method: Any | None=None, measurement_technique: Any | None=None, url: Any | None=None, variable_measured: Any | None=None) -> Assay:
    return Assay(id, identifier, about, comment, creator, has_part, measurement_method, measurement_technique, url, variable_measured)


__all__ = ["Assay_reflection"]

