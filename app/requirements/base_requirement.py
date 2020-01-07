
class BaseRequirement:

    def __init__(self, requirement_info):
        self.enforcements = requirement_info['enforcements']

    def is_valid_relationship(self, used_facts, relationship):
        """
        Checks if the used facts for a link match with the list of known fact relationships
        :param used_facts:
        :param relationship:
        :return: True if there is a match, False if not
        """
        if not self._check_edge(relationship.edge):
            return False
        for fact in used_facts:
            if self.check_fact(relationship.target, fact):
                return True
        return False

    def check_source(self, used_facts, relationship):
        """

        :param used_facts:
        :param relationship:
        :return:
        """
        for fact in used_facts:
            if self.check_fact(relationship.target, fact):
                return True
        return False

    @staticmethod
    def check_fact(target, match):
        if target[0] == match.trait and target[1] == match.value:
            return True
        return False

    """ PRIVATE """

    @staticmethod
    def _get_relationships(uf, relationships):
        return [r for r in relationships if r.source[0] == uf.trait and r.source[1] == uf.value]

    def _check_edge(self, edge):
        if edge == self.enforcements.edge:
            return True
        return False
