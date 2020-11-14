import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from jira_helper.wsgi import application  # noqa

app = application
