from lib.utilities import read_excel
from lib import defect, user_story
from config import CONFIG

# Add current directory to system path for module imports with relative paths
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    defects = read_excel(CONFIG.file_path_exported_defects)
    print('* Read defects from exported excel            ... Done')

    defects = defect.clean(defects)
    print('* Clean defects                               ... Done')

    defect.get_status_vs_severity(defects)
    print('* Export Status Vs Severity table             ... Done')
  
    user_stories = read_excel(CONFIG.file_path_exported_user_stories)
    print('* Read user stories from exported excel       ... Done')

    user_stories = user_story.clean(user_stories)
    print('* Clean user stories                          ... Done')
   
    sprint_summary = user_story.get_sprint_summary(user_stories)
    print('* Retrieving sprint summary                   ... Done')
   
    epic_summary = user_story.get_epic_summary(user_stories)
    print('* Retrieving epic summary                     ... Done')
   
if __name__== "__main__":
  main()
