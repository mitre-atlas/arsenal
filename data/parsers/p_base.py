import re


class Relationship:

    def __init__(self, source, edge, target):
        self.source = source
        self.edge = edge
        self.target = target

    def get_source(self):
        return self.source

    def get_relationship(self):
        return dict(source=self.source, edge=self.edge, target=self.target)


class BaseParser:

    @staticmethod
    def email(blob):
        """
        Parse out email addresses
        :param blob:
        :return:
        """
        return re.findall(r'[\w\.-]+@[\w\.-]+', blob)

    @staticmethod
    def line(blob):
        """
        Split a blob by line
        :param blob:
        :return:
        """
        return [x for x in blob.split('\n') if x]
