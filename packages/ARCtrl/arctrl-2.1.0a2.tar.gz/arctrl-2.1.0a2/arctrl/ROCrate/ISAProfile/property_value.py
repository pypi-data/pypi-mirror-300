from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1276() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.PropertyValue", None, PropertyValue, ROCrateObject_reflection())


class PropertyValue(ROCrateObject):
    def __init__(self, id: str, name: Any=None, value: Any=None, property_id: Any | None=None, unit_code: Any | None=None, unit_text: Any | None=None, value_reference: Any | None=None, additional_type: str | None=None) -> None:
        super().__init__(id, "schema.org/PropertyValue", additional_type)
        this: FSharpRef[PropertyValue] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_property("value", value, this.contents)
        set_optional_property("propertyID", property_id, this.contents)
        set_optional_property("unitCode", unit_code, this.contents)
        set_optional_property("unitText", unit_text, this.contents)
        set_optional_property("valueReference", value_reference, this.contents)


PropertyValue_reflection = _expr1276

def PropertyValue__ctor_7804003(id: str, name: Any=None, value: Any=None, property_id: Any | None=None, unit_code: Any | None=None, unit_text: Any | None=None, value_reference: Any | None=None, additional_type: str | None=None) -> PropertyValue:
    return PropertyValue(id, name, value, property_id, unit_code, unit_text, value_reference, additional_type)


__all__ = ["PropertyValue_reflection"]

