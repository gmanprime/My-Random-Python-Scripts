from qgis.core import *
from qgis.gui import *
import re

@qgsfunction(args='auto', group='Custom')
def filter_field_value(field_name, feature, possible_values, **kwargs):
    """
    Filter field value against a list of possible values using a regular expression.

    Example:
    filter_field_value('field_name', 'feature', 'possible_values')

    Returns:
    True if the field value matches any of the possible values, False otherwise.
    """
    field_value = feature[field_name]
    regex = '|'.join(possible_values)
    return bool(re.match(regex, field_value))