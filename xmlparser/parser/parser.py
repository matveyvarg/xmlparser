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

    def __init__(self, fields_to_find: Iterable[str]):
        self.fields_to_find = []
        self.attrs_to_find = []

        for field in fields_to_find:
            if '.' in field:
                self.attrs_to_find[tuple(field.split('.'))] = None
            else:
                self.fields_to_find[field] = None

    def checkNode(self, node: Element):
        """
        Check if it's the node we are looking for
        """
        if node.tag in self.fields_to_find:
            self.fields_to_find[node.tag] = node.text
        else:
            for tag, attr in self.attrs_to_find.keys():
                if node.tag == tag:
                    self.attrs_to_find[(tag, attr)] = node.attrib.get(attr)

    def parse_file(self, path: Union[str, Path]) -> dict:
        """
        Parse given file
        """

        root = ET.parse(path)

        for elem in root.iter():
            self.checkNode(iter)

        return dict(**self.fields_to_find, **self.attrs_to_find)
