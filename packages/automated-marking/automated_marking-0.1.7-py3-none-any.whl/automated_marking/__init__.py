# automated-marking/__init__.py

# Import functions or classes that you want to expose to users
from .language_utils import detect_language
from .java_utils import java_process
from .clone_utils import clone_or_pull_repo
from .logging_utils import log_results_to_excel
from .html_css_utils import html_css_proccess
from .sql_utils import find_and_check_sql_files

# You can also initialize variables or configurations here
__version__ = "0.1.7"
