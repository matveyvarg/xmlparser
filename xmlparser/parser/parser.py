import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element
from pathlib import Path
from typing import Union, Iterable

from xmlparser.utils import is_tuple_or_list

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

    def __init__(self, fields_to_find: Iterable[tuple]):
        self.fields_to_find = fields_to_find
        self.result = dict()

    def checkNode(self, node: Element):
        """
        Check if it's the node we are looking for
        """
        for field in self.fields_to_find:  # [(name, (attrs))]
            if node.tag == field[0]:
                if len(field) > 1 and is_tuple_or_list(field[1]):  # if attrs were setted
                    current = self.result.get(node.tag)  # If we've found such tag already
                    attrs = {k: node.attrib.get(k) for k in field[1]}
                    if current:
                        current.append(attrs)
                    else:
                        self.result[node.tag] = [attrs]
                else:  # if attrs were not setted
                    current = self.result.get(node.tag)
                    if current:
                        current.append(node.text)
                    else:
                        self.result[node.tag] = [node.text]

    def parse_file(self, path: Union[str, Path]) -> dict:
        """
        Parse given file
        """

        root = ET.parse(path)

        for elem in root.iter():
            self.checkNode(iter)

        return self.result
