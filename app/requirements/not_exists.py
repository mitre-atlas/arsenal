from plugins.stockpile.app.requirements.base_requirement import BaseRequirement


class Requirement(BaseRequirement):

    def enforce(self, link, relationships):
        """
        Given a link and all known fact relationships, check if the link's used fact combination complies
        with the abilities enforcement mechanism
        :param link
        :param relationships
        :return: True if it complies, False if it doesn't
        """
        for uf in link.used:
            if self.enforcements.source == uf.trait:
                for r in self._get_relationships(uf, relationships):
                    if self.is_valid_relationship([f for f in link.used if f != uf], r):
                        return False
        return True

