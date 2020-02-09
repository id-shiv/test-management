from lib.defects import clean, get_status_vs_severity
from lib.utilities import read_excel
from config import CONFIG

# Add current directory to system path for module imports with relative paths
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    defects = read_excel(CONFIG.file_path_exported_defects)
    print('* Read defects from exported excel            ... Done')

    defects = clean(defects)
    print('* Clean defects                               ... Done')

    get_status_vs_severity(defects)
    print('* Export Status Vs Severity table             ... Done')
  

if __name__== "__main__":
  main()
