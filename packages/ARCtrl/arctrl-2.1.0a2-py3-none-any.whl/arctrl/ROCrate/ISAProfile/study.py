from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from .dataset import (Dataset, Dataset_reflection)

def _expr1255() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Study", None, Study, Dataset_reflection())


class Study(Dataset):
    def __init__(self, id: str, identifier: Any=None, about: Any | None=None, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, description: Any | None=None, has_part: Any | None=None, headline: Any | None=None, url: Any | None=None) -> None:
        super().__init__(id, "Study")
        this: FSharpRef[Study] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("identifier", identifier, this.contents)
        set_optional_property("about", about, this.contents)
        set_optional_property("citation", citation, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("creator", creator, this.contents)
        set_optional_property("dateCreated", date_created, this.contents)
        set_optional_property("dateModified", date_modified, this.contents)
        set_optional_property("datePublished", date_published, this.contents)
        set_optional_property("description", description, this.contents)
        set_optional_property("hasPart", has_part, this.contents)
        set_optional_property("headline", headline, this.contents)
        set_optional_property("url", url, this.contents)


Study_reflection = _expr1255

def Study__ctor_Z3E174868(id: str, identifier: Any=None, about: Any | None=None, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, description: Any | None=None, has_part: Any | None=None, headline: Any | None=None, url: Any | None=None) -> Study:
    return Study(id, identifier, about, citation, comment, creator, date_created, date_modified, date_published, description, has_part, headline, url)


__all__ = ["Study_reflection"]

