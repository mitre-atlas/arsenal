from plugins.stockpile.app.requirements.base_requirement import BaseRequirement


class Requirement(BaseRequirement):

    def enforce(self, used_facts, relationships):
        """
        Given all used facts for a link and all known fact relationships, check if the used fact combination complies
        with the abilities enforcement mechanism
        :param used_facts
        :param relationships
        :return: True if it complies, False if it doesn't
        """
        for uf in used_facts:
            if self.enforcements.source == uf.trait:
                for r in self._get_relationships(uf, relationships):
                    if self.is_valid_relationship([f for f in used_facts if f != uf], r):
                        return True
        return False
