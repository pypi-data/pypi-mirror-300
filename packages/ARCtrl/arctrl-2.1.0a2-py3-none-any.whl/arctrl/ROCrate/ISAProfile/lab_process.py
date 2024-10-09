from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1257() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LabProcess", None, LabProcess, ROCrateObject_reflection())


class LabProcess(ROCrateObject):
    def __init__(self, id: str, name: Any=None, agent: Any=None, object: Any=None, result: Any=None, additional_type: str | None=None, executes_lab_protocol: Any | None=None, parameter_value: Any | None=None, end_time: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, "bioschemas.org/LabProcess", additional_type)
        this: FSharpRef[LabProcess] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_property("agent", agent, this.contents)
        set_property("object", object, this.contents)
        set_property("result", result, this.contents)
        set_optional_property("executesLabProtocol", executes_lab_protocol, this.contents)
        set_optional_property("parameterValue", parameter_value, this.contents)
        set_optional_property("endTime", end_time, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)


LabProcess_reflection = _expr1257

def LabProcess__ctor_Z33971C5D(id: str, name: Any=None, agent: Any=None, object: Any=None, result: Any=None, additional_type: str | None=None, executes_lab_protocol: Any | None=None, parameter_value: Any | None=None, end_time: Any | None=None, disambiguating_description: Any | None=None) -> LabProcess:
    return LabProcess(id, name, agent, object, result, additional_type, executes_lab_protocol, parameter_value, end_time, disambiguating_description)


__all__ = ["LabProcess_reflection"]

