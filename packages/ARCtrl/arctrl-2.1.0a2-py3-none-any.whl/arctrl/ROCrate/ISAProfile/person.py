from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1277() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Person", None, Person, ROCrateObject_reflection())


class Person(ROCrateObject):
    def __init__(self, id: str, given_name: Any=None, additional_type: str | None=None, family_name: Any | None=None, email: Any | None=None, identifier: Any | None=None, affiliation: Any | None=None, job_title: Any | None=None, additional_name: Any | None=None, address: Any | None=None, telephone: Any | None=None, fax_number: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, "schema.org/Person", additional_type)
        this: FSharpRef[Person] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("givenName", given_name, this.contents)
        set_optional_property("familyName", family_name, this.contents)
        set_optional_property("email", email, this.contents)
        set_optional_property("identifier", identifier, this.contents)
        set_optional_property("affiliation", affiliation, this.contents)
        set_optional_property("jobTitle", job_title, this.contents)
        set_optional_property("additionalName", additional_name, this.contents)
        set_optional_property("address", address, this.contents)
        set_optional_property("telephone", telephone, this.contents)
        set_optional_property("faxNumber", fax_number, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)


Person_reflection = _expr1277

def Person__ctor_Z45412208(id: str, given_name: Any=None, additional_type: str | None=None, family_name: Any | None=None, email: Any | None=None, identifier: Any | None=None, affiliation: Any | None=None, job_title: Any | None=None, additional_name: Any | None=None, address: Any | None=None, telephone: Any | None=None, fax_number: Any | None=None, disambiguating_description: Any | None=None) -> Person:
    return Person(id, given_name, additional_type, family_name, email, identifier, affiliation, job_title, additional_name, address, telephone, fax_number, disambiguating_description)


__all__ = ["Person_reflection"]

