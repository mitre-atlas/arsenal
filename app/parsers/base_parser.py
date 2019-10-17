import re


class BaseParser:

    @staticmethod
    def set_value(search, match, used_facts):
        """
        Determine the value of a source/target for a Relationship
        :param search: a fact property to look for; either a source or target fact
        :param match: a parsing match
        :param used_facts: a list of facts that were used in a command
        :return: either None, the value of a matched used_fact, or the parsing match
        """
        if not search:
            return None
        for uf in used_facts:
            if search == uf['property']:
                return uf['value']
        return match

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
