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

    def get_attrs(self, node, attrs) -> dict:
        return {k: node.attrib[k] for k in attrs if k in node.attrib.keys()}


    def checkNode(self, node: Element):
        """
        Check if it's the node we are looking for
        """
        for field in self.fields_to_find:  # [(name, (attrs), (children, (attrs)))]
            tag = node.tag[node.tag.index('}')+1:]
            if tag == field[0]:
                current = self.result.get(tag)  # If we've found such tag already
                print(field)
                if len(field) > 1 and is_tuple_or_list(field[1]):  # if attrs were setted
                    # Find info in childers
                    child_info = {}
                    for children, child_attrs in field[2:]:
                        child_node = node.find(children)
                        child_info[children] = child_node.text
                        child_info.update(self.get_attrs(child_node, child_attrs))
                    print(field[1])
                    if current:
                        current.append(dict(**self.get_attrs(node, field[1]), **child_info))
                    else:
                        self.result[tag] = [self.get_attrs(node, field[1])]

                else:  # if attrs were not setted
                    if current:
                        current.append(node.text)
                    else:
                        self.result[tag] = [node.text]

    def parse_file(self, path: Union[str, Path]) -> dict:
        """
        Parse given file
        """

        root = ET.parse(path)

        for elem in root.iter():
            self.checkNode(elem)

        return self.result
