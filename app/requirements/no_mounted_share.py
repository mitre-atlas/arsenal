from plugins.stockpile.app.requirements.base_requirement import BaseRequirement


class Requirement(BaseRequirement):

    def enforce(self, link, relationships):
        """
        Given a link and relationships ensure that there is NO existence of the enforced relationships
        :param link
        :param relationships
        :return: True if it complies, False if it doesn't
        """
        for uf in link.used:
            if self.enforcements.source == uf.trait:
                for r in relationships:
                    if r.source[0] == self.enforcements.source == self.check_fact(r.source, uf):
                        return False
        return True
