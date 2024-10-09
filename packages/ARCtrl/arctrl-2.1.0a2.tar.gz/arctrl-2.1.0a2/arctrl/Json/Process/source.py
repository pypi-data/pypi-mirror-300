from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, list_1 as list_1_2, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.Process.material_attribute_value import MaterialAttributeValue
from ...Core.Process.source import Source
from ...Core.uri import URIModule_toString
from ..context.rocrate.isa_source_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from .material_attribute_value import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def ROCrate_genID(s: Source) -> str:
    match_value: str | None = s.ID
    if match_value is None:
        match_value_1: str | None = s.Name
        if match_value_1 is None:
            return "#EmptySource"

        else: 
            return "#Source_" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def ROCrate_encoder(oa: Source) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2187(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2186(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2186()

    class ObjectExpr2188(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Source")

    def _arrow2190(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2189(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2189()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2187()), ("@type", list_1_1(singleton(ObjectExpr2188()))), try_include("name", _arrow2190, oa.Name), try_include_list_opt("characteristics", ROCrate_encoder_1, oa.Characteristics), ("@context", context_jsonvalue)]))
    class ObjectExpr2191(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2191()


def _arrow2195(get: IGetters) -> Source:
    def _arrow2192(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2193(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2194(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
        arg_5: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ROCrate_decoder_1)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("characteristics", arg_5)

    return Source(_arrow2192(), _arrow2193(), _arrow2194())


ROCrate_decoder: Decoder_1[Source] = object(_arrow2195)

def ISAJson_encoder(id_map: Any | None, oa: Source) -> IEncodable:
    def f(oa_1: Source, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2199(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2198(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2198()

        def _arrow2201(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2200(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2200()

        def _arrow2202(oa_2: MaterialAttributeValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(id_map, oa_2)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2199, ROCrate_genID(oa_1)), try_include("name", _arrow2201, oa_1.Name), try_include_list_opt("characteristics", _arrow2202, oa_1.Characteristics)]))
        class ObjectExpr2203(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2203()

    if id_map is not None:
        def _arrow2204(s_1: Source, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(s_1)

        return encode(_arrow2204, f, oa, id_map)

    else: 
        return f(oa)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "characteristics", "@type", "@context"])

def _arrow2208(get: IGetters) -> Source:
    def _arrow2205(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2206(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2207(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
        arg_5: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ISAJson_decoder_1)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("characteristics", arg_5)

    return Source(_arrow2205(), _arrow2206(), _arrow2207())


ISAJson_decoder: Decoder_1[Source] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2208)

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

