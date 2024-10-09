from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1275() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Data", None, Data, ROCrateObject_reflection())


class Data(ROCrateObject):
    def __init__(self, id: str, name: Any=None, additional_type: str | None=None, comment: Any | None=None, encoding_format: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, "schema.org/MediaObject", additional_type)
        this: FSharpRef[Data] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("encodingFormat", encoding_format, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)


Data_reflection = _expr1275

def Data__ctor_Z68810720(id: str, name: Any=None, additional_type: str | None=None, comment: Any | None=None, encoding_format: Any | None=None, disambiguating_description: Any | None=None) -> Data:
    return Data(id, name, additional_type, comment, encoding_format, disambiguating_description)


__all__ = ["Data_reflection"]

