from plugins.stockpile.app.requirements.base_requirement import BaseRequirement


class Requirement(BaseRequirement):

    def enforce(self, link, relationships):
        """
        Given a link, check if any of the used facts must comply with paw provenance requirements
        :param link
        :param relationships
        :return: True if it complies, False if it doesn't
        """
        for uf in link.used:
            if self.enforcements.source == uf.trait:
                if link.paw == uf.collected_by:
                    return True
        return False
