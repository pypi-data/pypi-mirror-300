from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.util import to_enumerable
from .collections_ import (Dictionary_ofSeq, Dictionary_tryFind)

def OntobeeParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.obolibrary.org/obo/") + "") + tsr) + "_") + local_tan) + ""


def BioregistryParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://bioregistry.io/") + "") + tsr) + ":") + local_tan) + ""


def OntobeeDPBOParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.org/nfdi4plants/ontology/dpbo/") + "") + tsr) + "_") + local_tan) + ""


def MSParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ms/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def POParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/po/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def ROParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ro/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def _arrow456(tsr: str) -> Callable[[str], str]:
    def _arrow455(local_tan: str) -> str:
        return OntobeeDPBOParser(tsr, local_tan)

    return _arrow455


def _arrow458(tsr_1: str) -> Callable[[str], str]:
    def _arrow457(local_tan_1: str) -> str:
        return MSParser(tsr_1, local_tan_1)

    return _arrow457


def _arrow460(tsr_2: str) -> Callable[[str], str]:
    def _arrow459(local_tan_2: str) -> str:
        return POParser(tsr_2, local_tan_2)

    return _arrow459


def _arrow462(tsr_3: str) -> Callable[[str], str]:
    def _arrow461(local_tan_3: str) -> str:
        return ROParser(tsr_3, local_tan_3)

    return _arrow461


def _arrow464(tsr_4: str) -> Callable[[str], str]:
    def _arrow463(local_tan_4: str) -> str:
        return BioregistryParser(tsr_4, local_tan_4)

    return _arrow463


def _arrow466(tsr_5: str) -> Callable[[str], str]:
    def _arrow465(local_tan_5: str) -> str:
        return BioregistryParser(tsr_5, local_tan_5)

    return _arrow465


def _arrow468(tsr_6: str) -> Callable[[str], str]:
    def _arrow467(local_tan_6: str) -> str:
        return BioregistryParser(tsr_6, local_tan_6)

    return _arrow467


def _arrow470(tsr_7: str) -> Callable[[str], str]:
    def _arrow469(local_tan_7: str) -> str:
        return BioregistryParser(tsr_7, local_tan_7)

    return _arrow469


def _arrow472(tsr_8: str) -> Callable[[str], str]:
    def _arrow471(local_tan_8: str) -> str:
        return BioregistryParser(tsr_8, local_tan_8)

    return _arrow471


def _arrow474(tsr_9: str) -> Callable[[str], str]:
    def _arrow473(local_tan_9: str) -> str:
        return BioregistryParser(tsr_9, local_tan_9)

    return _arrow473


def _arrow476(tsr_10: str) -> Callable[[str], str]:
    def _arrow475(local_tan_10: str) -> str:
        return BioregistryParser(tsr_10, local_tan_10)

    return _arrow475


def _arrow478(tsr_11: str) -> Callable[[str], str]:
    def _arrow477(local_tan_11: str) -> str:
        return BioregistryParser(tsr_11, local_tan_11)

    return _arrow477


def _arrow480(tsr_12: str) -> Callable[[str], str]:
    def _arrow479(local_tan_12: str) -> str:
        return BioregistryParser(tsr_12, local_tan_12)

    return _arrow479


def _arrow482(tsr_13: str) -> Callable[[str], str]:
    def _arrow481(local_tan_13: str) -> str:
        return BioregistryParser(tsr_13, local_tan_13)

    return _arrow481


def _arrow484(tsr_14: str) -> Callable[[str], str]:
    def _arrow483(local_tan_14: str) -> str:
        return BioregistryParser(tsr_14, local_tan_14)

    return _arrow483


uri_parser_collection: Any = Dictionary_ofSeq(to_enumerable([("DPBO", _arrow456), ("MS", _arrow458), ("PO", _arrow460), ("RO", _arrow462), ("ENVO", _arrow464), ("CHEBI", _arrow466), ("GO", _arrow468), ("OBI", _arrow470), ("PATO", _arrow472), ("PECO", _arrow474), ("TO", _arrow476), ("UO", _arrow478), ("EFO", _arrow480), ("NCIT", _arrow482), ("OMP", _arrow484)]))

def create_oauri(tsr: str, local_tan: str) -> str:
    match_value: Callable[[str, str], str] | None = Dictionary_tryFind(tsr, uri_parser_collection)
    if match_value is None:
        return OntobeeParser(tsr, local_tan)

    else: 
        return match_value(tsr)(local_tan)



__all__ = ["OntobeeParser", "BioregistryParser", "OntobeeDPBOParser", "MSParser", "POParser", "ROParser", "uri_parser_collection", "create_oauri"]

