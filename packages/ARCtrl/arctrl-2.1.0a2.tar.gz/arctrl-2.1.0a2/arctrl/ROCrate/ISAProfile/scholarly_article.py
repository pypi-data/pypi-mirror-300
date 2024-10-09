from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..rocrate_object import (ROCrateObject, ROCrateObject_reflection)

def _expr1278() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.ScholarlyArticle", None, ScholarlyArticle, ROCrateObject_reflection())


class ScholarlyArticle(ROCrateObject):
    def __init__(self, id: str, headline: Any=None, identifier: Any=None, additional_type: str | None=None, author: Any | None=None, url: Any | None=None, creative_work_status: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, "schema.org/ScholarlyArticle", additional_type)
        this: FSharpRef[ScholarlyArticle] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("headline", headline, this.contents)
        set_property("identifier", identifier, this.contents)
        set_optional_property("author", author, this.contents)
        set_optional_property("url", url, this.contents)
        set_optional_property("creativeWorkStatus", creative_work_status, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)


ScholarlyArticle_reflection = _expr1278

def ScholarlyArticle__ctor_11693003(id: str, headline: Any=None, identifier: Any=None, additional_type: str | None=None, author: Any | None=None, url: Any | None=None, creative_work_status: Any | None=None, disambiguating_description: Any | None=None) -> ScholarlyArticle:
    return ScholarlyArticle(id, headline, identifier, additional_type, author, url, creative_work_status, disambiguating_description)


__all__ = ["ScholarlyArticle_reflection"]

