from utilities.choices import ChoiceSet

class StatusChoices(ChoiceSet):
    #key = 'MyModel.status'

    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    STATUS_UNKNOWN = 'unknown'
    STATUS_UNCHECKED = 'no_lldp_response'
    STATUS_OBSOLETE = 'obsolete'

    CHOICES = [
        (STATUS_PASSED, 'Passed'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_UNKNOWN, 'Unknown'),
        (STATUS_UNCHECKED, 'No LLDP Response'),
        (STATUS_OBSOLETE, 'Obsolete'),
    ]