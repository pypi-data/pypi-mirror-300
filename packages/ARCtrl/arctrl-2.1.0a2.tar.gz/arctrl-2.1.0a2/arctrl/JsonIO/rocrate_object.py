from __future__ import annotations
from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import fold
from ..fable_modules.fable_library.list import (FSharpList, is_empty, length, head, of_array)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (to_list, delay, map, enumerate_from_functions)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, is_iterable, get_enumerator, IEnumerator, IEnumerable_1, int32_to_string)
from ..fable_modules.thoth_json_core.decode import (Getters_2__ctor_Z4BE6C149, Getters_2, IGetters, IRequiredGetter, string, Getters_2__get_Errors, one_of, map as map_1, int_1, decimal)
from ..fable_modules.thoth_json_core.encode import list_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ..Json.decode import Helpers_prependPath
from ..Json.encode import date_time
from ..ROCrate.rocrate_object import (ROCrateObject, ROCrateObject__ctor_Z2FC25A28)

__A_ = TypeVar("__A_")

def generic_encoder(obj: Any=None) -> IEncodable:
    if str(type(obj)) == "<class \'str\'>":
        class ObjectExpr3074(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers.encode_string(obj)

        return ObjectExpr3074()

    elif str(type(obj)) == "<class \'int\'>":
        class ObjectExpr3075(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_1.encode_signed_integral_number(obj)

        return ObjectExpr3075()

    elif str(type(obj)) == "<class \'bool\'>":
        class ObjectExpr3076(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_2.encode_bool(obj)

        return ObjectExpr3076()

    elif str(type(obj)) == "<class \'float\'>":
        class ObjectExpr3077(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_3.encode_decimal_number(obj)

        return ObjectExpr3077()

    elif isinstance(obj, datetime):
        return date_time(obj)

    elif isinstance(obj, ROCrateObject):
        return encoder(obj)

    elif equals(obj, None):
        class ObjectExpr3078(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
                return helpers_4.encode_null()

        return ObjectExpr3078()

    elif is_iterable(obj):
        def _arrow3082(__unit: None=None, obj: Any=obj) -> IEnumerable_1[IEncodable]:
            def _arrow3079(__unit: None=None) -> IEnumerator[Any]:
                return get_enumerator(obj)

            def _arrow3080(enumerator: IEnumerator[Any]) -> bool:
                return enumerator.System_Collections_IEnumerator_MoveNext()

            def _arrow3081(enumerator_1: IEnumerator[Any]) -> Any:
                return enumerator_1.System_Collections_IEnumerator_get_Current()

            return map(generic_encoder, enumerate_from_functions(_arrow3079, _arrow3080, _arrow3081))

        return list_1(to_list(delay(_arrow3082)))

    else: 
        raise Exception("Unknown type")



def encoder(obj: ROCrateObject) -> IEncodable:
    def mapping(kv: Any, obj: Any=obj) -> tuple[str, IEncodable]:
        return (kv[0], generic_encoder(obj))

    values: IEnumerable_1[tuple[str, IEncodable]] = map(mapping, obj.GetProperties(True))
    class ObjectExpr3083(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr3083()


def _arrow3096(__unit: None=None) -> Decoder_1[Any]:
    def decode(__unit: None=None) -> Decoder_1[Any]:
        class ObjectExpr3087(Decoder_1[ROCrateObject]):
            def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any) -> FSharpResult_2[ROCrateObject, tuple[str, ErrorReason_1[__A_]]]:
                if helpers.is_object(value):
                    getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
                    properties: IEnumerable_1[str] = helpers.get_properties(value)
                    result: ROCrateObject
                    get: IGetters = getters
                    def _arrow3084(__unit: None=None) -> str:
                        object_arg: IRequiredGetter = get.Required
                        return object_arg.Field("@id", string)

                    def _arrow3085(__unit: None=None) -> str:
                        object_arg_1: IRequiredGetter = get.Required
                        return object_arg_1.Field("@type", string)

                    o: ROCrateObject = ROCrateObject__ctor_Z2FC25A28(_arrow3084(), _arrow3085())
                    with get_enumerator(properties) as enumerator:
                        while enumerator.System_Collections_IEnumerator_MoveNext():
                            property: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                            if (property != "@type") if (property != "@id") else False:
                                def _arrow3086(__unit: None=None) -> Any:
                                    arg_5: Decoder_1[Any] = decode(None)
                                    object_arg_2: IRequiredGetter = get.Required
                                    return object_arg_2.Field(property, arg_5)

                                o.SetProperty(property, _arrow3086())

                    result = o
                    match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
                    if not is_empty(match_value):
                        errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                        return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head(match_value))

                    else: 
                        return FSharpResult_2(0, result)


                else: 
                    return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))


        decode_object: Decoder_1[ROCrateObject] = ObjectExpr3087()
        class ObjectExpr3089(Decoder_1[Array[Any]]):
            def Decode(self, helpers_1: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]]:
                if helpers_1.is_array(value_1):
                    i: int = -1
                    def folder(acc: FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]], value_2: __A_) -> FSharpResult_2[Array[Any], tuple[str, ErrorReason_1[__A_]]]:
                        nonlocal i
                        i = (i + 1) or 0
                        if acc.tag == 0:
                            acc_1: Array[Any] = acc.fields[0]
                            match_value_1: FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]
                            copy_of_struct: Decoder_1[Any] = decode(None)
                            match_value_1 = copy_of_struct.Decode(helpers_1, value_2)
                            if match_value_1.tag == 0:
                                (acc_1.append(match_value_1.fields[0]))
                                return FSharpResult_2(0, acc_1)

                            else: 
                                def _arrow3088(__unit: None=None, acc: Any=acc, value_2: Any=value_2) -> tuple[str, ErrorReason_1[__A_]]:
                                    tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value_1.fields[0]
                                    return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                                return FSharpResult_2(1, _arrow3088())


                        else: 
                            return acc


                    return fold(folder, FSharpResult_2(0, []), helpers_1.as_array(value_1))

                else: 
                    return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value_1)))


        resize_array: Decoder_1[Array[Any]] = ObjectExpr3089()
        def _arrow3091(value_4: ROCrateObject) -> Any:
            return value_4

        def _arrow3092(value_5: Array[Any]) -> Any:
            return value_5

        def _arrow3093(value_6: str) -> Any:
            return value_6

        def _arrow3094(value_7: int) -> Any:
            return value_7

        def _arrow3095(value_8: Decimal) -> Any:
            return value_8

        return one_of(of_array([map_1(_arrow3091, decode_object), map_1(_arrow3092, resize_array), map_1(_arrow3093, string), map_1(_arrow3094, int_1), map_1(_arrow3095, decimal)]))

    return decode(None)


decoder: Decoder_1[Any] = _arrow3096()

__all__ = ["generic_encoder", "encoder", "decoder"]

