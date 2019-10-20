from plugins.stockpile.app.requirements.base_requirement import BaseRequirement


class Requirement(BaseRequirement):

    def enforce(self, potential_fact, used_facts, all_operation_facts):
        """
        Given a potential fact, all facts used by the current link and all operation facts, determine if it complies
        with this fact relationships enforcement mechanism
        :param potential_fact
        :param used_facts
        :param all_operation_facts
        :return: True if it complies, False if it doesn't
        """
        for uf in used_facts:
            f = self._get_fact(all_operation_facts, uf)
            if not self.check_source_target(f, potential_fact):
                return False
        return True

    """ PRIVATE """

    @staticmethod
    def _get_fact(fact_list, fact_id):
        return next((f for f in fact_list if f['id'] == fact_id), False)

