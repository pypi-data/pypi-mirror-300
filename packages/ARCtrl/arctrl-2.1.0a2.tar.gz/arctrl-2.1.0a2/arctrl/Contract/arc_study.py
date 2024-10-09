from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.list import FSharpList
from ..fable_modules.fable_library.option import (default_arg, value)
from ..fable_modules.fable_library.seq import (to_array, delay, append, collect, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, safe_hash)
from ..Core.arc_types import (ArcStudy, ArcAssay)
from ..Core.data_map import (DataMap, DataMap__set_StaticHash_Z524259A4, DataMap__get_StaticHash)
from ..Core.Helper.identifier import Study_fileNameFromIdentifier
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import (combine_many, get_study_folder_path)
from ..Spreadsheet.arc_study import (ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522, ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D)
from .contract import (DTO, Contract, DTOType)
from .datamap import (ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5)

def _007CStudyPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow2950(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow2950, input, None)) else False:
        if input[0] == "studies":
            if input[2] == "isa.study.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_study_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcStudy__ArcStudy_ToCreateContract_66CF920(this: ArcStudy, WithFolder: bool | None=None, datamap_as_file: bool | None=None) -> Array[Contract]:
    with_folder: bool = default_arg(WithFolder, False)
    data_map_as_file: bool = default_arg(datamap_as_file, False)
    path: str = Study_fileNameFromIdentifier(this.Identifier)
    dto: DTO = DTO(0, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(this, None, not data_map_as_file))
    c: Contract = Contract.create_create(path, DTOType(1), dto)
    def _arrow2956(__unit: None=None, this: Any=this, WithFolder: Any=WithFolder, datamap_as_file: Any=datamap_as_file) -> IEnumerable_1[Contract]:
        def _arrow2952(__unit: None=None) -> IEnumerable_1[Contract]:
            folder_fs: FileSystemTree = FileSystemTree.create_studies_folder([FileSystemTree.create_study_folder(this.Identifier)])
            def _arrow2951(p: str) -> IEnumerable_1[Contract]:
                return singleton(Contract.create_create(p, DTOType(8))) if ((p != "studies/.gitkeep") if (p != path) else False) else empty()

            return collect(_arrow2951, folder_fs.ToFilePaths(False))

        def _arrow2955(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2953(__unit: None=None) -> IEnumerable_1[Contract]:
                match_value: DataMap | None = this.DataMap
                if match_value is not None:
                    dm: DataMap = match_value
                    DataMap__set_StaticHash_Z524259A4(dm, safe_hash(dm))
                    return singleton(ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5(dm, this.Identifier)) if data_map_as_file else empty()

                else: 
                    return empty()


            def _arrow2954(__unit: None=None) -> IEnumerable_1[Contract]:
                return singleton(c)

            return append(_arrow2953(), delay(_arrow2954))

        return append(_arrow2952() if with_folder else empty(), delay(_arrow2955))

    return to_array(delay(_arrow2956))


def ARCtrl_ArcStudy__ArcStudy_ToUpdateContract_6FCE9E49(this: ArcStudy, datamap_as_file: bool | None=None) -> Array[Contract]:
    datamap_as_file_1: bool = default_arg(datamap_as_file, False)
    path: str = Study_fileNameFromIdentifier(this.Identifier)
    hash_1: int = this.GetLightHashCode() or 0
    datamap_has_changed: bool
    match_value: DataMap | None = this.DataMap
    if match_value is not None:
        dm: DataMap = match_value
        hc: bool = safe_hash(dm) != DataMap__get_StaticHash(dm)
        DataMap__set_StaticHash_Z524259A4(dm, safe_hash(dm))
        datamap_has_changed = hc

    else: 
        datamap_has_changed = False

    def _arrow2959(__unit: None=None, this: Any=this, datamap_as_file: Any=datamap_as_file) -> IEnumerable_1[Contract]:
        def _arrow2957(__unit: None=None) -> Contract:
            dto: DTO = DTO(0, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(this, None, not datamap_as_file_1))
            return Contract.create_update(path, DTOType(1), dto)

        def _arrow2958(__unit: None=None) -> IEnumerable_1[Contract]:
            return singleton(ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5(value(this.DataMap), this.Identifier)) if (datamap_as_file_1 if datamap_has_changed else False) else empty()

        return append(singleton(_arrow2957()) if (True if (hash_1 != this.StaticHash) else ((not datamap_as_file_1) if datamap_has_changed else False)) else empty(), delay(_arrow2958))

    return to_array(delay(_arrow2959))


def ARCtrl_ArcStudy__ArcStudy_ToDeleteContract(this: ArcStudy) -> Contract:
    path: str = get_study_folder_path(this.Identifier)
    return Contract.create_delete(path)


def ARCtrl_ArcStudy__ArcStudy_toDeleteContract_Static_1680536E(study: ArcStudy) -> Contract:
    return ARCtrl_ArcStudy__ArcStudy_ToDeleteContract(study)


def ARCtrl_ArcStudy__ArcStudy_toCreateContract_Static_Z76BBA099(study: ArcStudy, WithFolder: bool | None=None) -> Array[Contract]:
    return ARCtrl_ArcStudy__ArcStudy_ToCreateContract_66CF920(study, WithFolder)


def ARCtrl_ArcStudy__ArcStudy_toUpdateContract_Static_1680536E(study: ArcStudy) -> Array[Contract]:
    return ARCtrl_ArcStudy__ArcStudy_ToUpdateContract_6FCE9E49(study)


def ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F(c: Contract) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 1:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        pattern_matching_result = 0
                        fsworkbook = c.DTO.fields[0]

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CStudyPath_007C__007C", "ARCtrl_ArcStudy__ArcStudy_ToCreateContract_66CF920", "ARCtrl_ArcStudy__ArcStudy_ToUpdateContract_6FCE9E49", "ARCtrl_ArcStudy__ArcStudy_ToDeleteContract", "ARCtrl_ArcStudy__ArcStudy_toDeleteContract_Static_1680536E", "ARCtrl_ArcStudy__ArcStudy_toCreateContract_Static_Z76BBA099", "ARCtrl_ArcStudy__ArcStudy_toUpdateContract_Static_1680536E", "ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F"]

