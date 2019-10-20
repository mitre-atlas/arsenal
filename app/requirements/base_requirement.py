
class BaseRequirement:

    def __init__(self, requirement_info):
        self.enforcements = requirement_info['enforcements']

    def check_source_target(self, source, target):
        """
        Give a source and target fact, return
        :param source: A fact object
        :param target: A fact object
        :return: True if the source and target comply with the enforcement mechanism or if the enforcement mechanism
        doesn't apply to the parameter facts. False if the parameter facts don't comply
        """
        if self._check_requirement_type(source, target):
            if self._is_valid_relationship(source, target):
                return True
            return False
        return True

    """ PRIVATE """

    def _check_requirement_type(self, source, target):
        if self.enforcements.get('source') == source.get('property') and self.enforcements.get('target') == \
                target.get('property'):
            return True
        return False

    def _is_valid_relationship(self, source, target):
        relationships = [relationship.get('target') for relationship in source.get('relationships', [])
                         if self.enforcements.get('edge') == relationship.get('edge')]
        return next((True for r in relationships if r.get('value') == target.get('value')), False)
