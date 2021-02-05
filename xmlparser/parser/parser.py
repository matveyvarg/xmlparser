import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element
from pathlib import Path
from typing import Union, Iterable


class IBaseParser:
    """
    Base Abastract Class for Parser
    """

    def parse_file(path: Union[str, Path]):
        """
        Parse file and return data
        """
        raise NotImplementedError


class XMLParser(IBaseParser):
    """
    Parser for XML files
    """

    def __init__(self, fields_to_find: Iterable[str])
        self.

    def parse_file(self, path: Union[str, Path]):
        """
        Parse given file
        """

        root = ET.parse(path)


        