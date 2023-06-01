from qgis.core import *
from qgis.gui import *
import re

@qgsfunction(args='auto', group='Custom')
def regexFilter(expression, feature, *possVals, **kwargs):
    """
    Filter field value against a list of possible values using regular expression.

    <h3>Parameters:</h3>
    <ul>
        <li><code>expression</code>: The expression used to specify the field name.</li>
        <li><code>feature</code>: The feature to filter.</li>
        <li><code>possible_values_strings</code>: The list of possible values to match against.</li>
    </ul>

    <h3>Returns:</h3>
    <p>True if field value matches any of the possible values, False otherwise.</p>

    <h3>Examples:</h3>
    <p>Filter all features where the 'name' field matches either 'John' or 'Jane':</p>
    <pre>
        regexFilter('name', $currentfeature, 'John', 'Jane')
    </pre>

    <p>Filter all features where the 'age' field matches a number between 18 and 30:</p>
    <pre>
        regexFilter('age', $currentfeature, '[1-2][8-9]|[3][0]')
    </pre>

    <p>Filter all features where the 'email' field matches a valid email address:</p>
    <pre>
        regexFilter('email', $currentfeature, '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    </pre>
    """
    # Get field value
    field_value = QgsExpression(expression).evaluate(feature)

    # Convert possible values strings into a list
    possible_values = [value.strip() for value in possVals]

    # Check if field value matches any of the possible values
    for value in possible_values:
        if re.match(value, str(field_value)):
            return True

    return False