from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.option import (default_arg, value)
from ..fable_modules.fable_library.seq import (to_array, delay, append, collect, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, safe_hash)
from ..Core.arc_types import ArcAssay
from ..Core.data_map import (DataMap, DataMap__set_StaticHash_Z524259A4, DataMap__get_StaticHash)
from ..Core.Helper.identifier import Assay_fileNameFromIdentifier
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import (combine_many, get_assay_folder_path)
from ..Spreadsheet.arc_assay import (ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F, ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D)
from .contract import (DTO, Contract, DTOType)
from .datamap import (ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5)

def _007CAssayPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow2961(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow2961, input, None)) else False:
        if input[0] == "assays":
            if input[2] == "isa.assay.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_assay_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcAssay__ArcAssay_ToCreateContract_66CF920(this: ArcAssay, WithFolder: bool | None=None, datamap_as_file: bool | None=None) -> Array[Contract]:
    with_folder: bool = default_arg(WithFolder, False)
    data_map_as_file: bool = default_arg(datamap_as_file, False)
    path: str = Assay_fileNameFromIdentifier(this.Identifier)
    dto: DTO = DTO(0, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(this, not data_map_as_file))
    c: Contract = Contract.create_create(path, DTOType(0), dto)
    def _arrow2967(__unit: None=None, this: Any=this, WithFolder: Any=WithFolder, datamap_as_file: Any=datamap_as_file) -> IEnumerable_1[Contract]:
        def _arrow2963(__unit: None=None) -> IEnumerable_1[Contract]:
            folder_fs: FileSystemTree = FileSystemTree.create_assays_folder([FileSystemTree.create_assay_folder(this.Identifier)])
            def _arrow2962(p: str) -> IEnumerable_1[Contract]:
                return singleton(Contract.create_create(p, DTOType(8))) if ((p != "assays/.gitkeep") if (p != path) else False) else empty()

            return collect(_arrow2962, folder_fs.ToFilePaths(False))

        def _arrow2966(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2964(__unit: None=None) -> IEnumerable_1[Contract]:
                match_value: DataMap | None = this.DataMap
                if match_value is not None:
                    dm: DataMap = match_value
                    DataMap__set_StaticHash_Z524259A4(dm, safe_hash(dm))
                    return singleton(ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5(dm, this.Identifier)) if data_map_as_file else empty()

                else: 
                    return empty()


            def _arrow2965(__unit: None=None) -> IEnumerable_1[Contract]:
                return singleton(c)

            return append(_arrow2964(), delay(_arrow2965))

        return append(_arrow2963() if with_folder else empty(), delay(_arrow2966))

    return to_array(delay(_arrow2967))


def ARCtrl_ArcAssay__ArcAssay_ToUpdateContract_6FCE9E49(this: ArcAssay, datamap_as_file: bool | None=None) -> Array[Contract]:
    datamap_as_file_1: bool = default_arg(datamap_as_file, False)
    path: str = Assay_fileNameFromIdentifier(this.Identifier)
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

    def _arrow2970(__unit: None=None, this: Any=this, datamap_as_file: Any=datamap_as_file) -> IEnumerable_1[Contract]:
        def _arrow2968(__unit: None=None) -> Contract:
            dto: DTO = DTO(0, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(this, not datamap_as_file_1))
            return Contract.create_update(path, DTOType(0), dto)

        def _arrow2969(__unit: None=None) -> IEnumerable_1[Contract]:
            return singleton(ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5(value(this.DataMap), this.Identifier)) if (datamap_as_file_1 if datamap_has_changed else False) else empty()

        return append(singleton(_arrow2968()) if (True if (hash_1 != this.StaticHash) else ((not datamap_as_file_1) if datamap_has_changed else False)) else empty(), delay(_arrow2969))

    return to_array(delay(_arrow2970))


def ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(this: ArcAssay) -> Contract:
    path: str = get_assay_folder_path(this.Identifier)
    return Contract.create_delete(path)


def ARCtrl_ArcAssay__ArcAssay_toDeleteContract_Static_1501C0F8(assay: ArcAssay) -> Contract:
    return ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(assay)


def ARCtrl_ArcAssay__ArcAssay_toCreateContract_Static_Z2508BE4F(assay: ArcAssay, WithFolder: bool | None=None) -> Array[Contract]:
    return ARCtrl_ArcAssay__ArcAssay_ToCreateContract_66CF920(assay, WithFolder)


def ARCtrl_ArcAssay__ArcAssay_toUpdateContract_Static_1501C0F8(assay: ArcAssay) -> Array[Contract]:
    return ARCtrl_ArcAssay__ArcAssay_ToUpdateContract_6FCE9E49(assay)


def ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F(c: Contract) -> ArcAssay | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 0:
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
        return ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CAssayPath_007C__007C", "ARCtrl_ArcAssay__ArcAssay_ToCreateContract_66CF920", "ARCtrl_ArcAssay__ArcAssay_ToUpdateContract_6FCE9E49", "ARCtrl_ArcAssay__ArcAssay_ToDeleteContract", "ARCtrl_ArcAssay__ArcAssay_toDeleteContract_Static_1501C0F8", "ARCtrl_ArcAssay__ArcAssay_toCreateContract_Static_Z2508BE4F", "ARCtrl_ArcAssay__ArcAssay_toUpdateContract_Static_1501C0F8", "ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F"]

