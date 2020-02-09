import pandas as pd
import matplotlib.pyplot as plt

from config import CONFIG, USER_STORIES


def clean(user_stories):
    ## Get the user stories data ready for processing
    # Rename the column names to standarize (based on PARAMETER MAPPING)
    mapping = {value: key for key, value in USER_STORIES.PARAMETER_MAPPING.__dict__.items() if not key.startswith('__') and not callable(key)}
    user_stories = user_stories.rename(columns = mapping)

    # Rename status to standardize the names (based on STATUS)
    mapping = {value: key for key, value in USER_STORIES.STATUS.__dict__.items() if not key.startswith('__') and not callable(key)}
    user_stories = user_stories.replace(mapping)

    user_stories['count'] = 1 # add a column 'count' to get the count while deriving charts

    user_stories = user_stories.fillna(0) # fill empty cell values with 0

    ## View the data before processing
    # print(user_stories)
    # print(user_stories.shape)
    # print(user_stories.describe())
    # print(user_stories.info())
    return user_stories

def get_sprint_summary(user_stories, return_type='csv'):
    ## Get reports

    # Get sprint summary, status vs sprint vs story points
    sprint = user_stories.pivot(index='status', columns='sprint', values='story_points').fillna(0)

    # Total story points per sprint 
    sprint.loc['Total', :] = sprint.sum(axis=0)

    # Total story points per status
    sprint.loc[:, 'Total'] = sprint.sum(axis=1)

    sprint= sprint.astype('int32')

    if return_type == 'table':
        return sprint
    elif return_type == 'csv':
        sprint.to_csv(CONFIG.file_path_sprint_us_summary)

def get_epic_summary(user_stories, return_type='csv'):
    ## Get reports

    # Get epic summary, status vs epic vs story points
    epic = user_stories.pivot(index='linked_epic', columns='status', values='story_points').fillna(0)

    # Total story points per epic 
    epic.loc['Total', :] = epic.sum(axis=0)

    # Total story points per status
    epic.loc[:, 'Total'] = epic.sum(axis=1)

    epic = epic.astype('int32')

    if return_type == 'table':
        return epic
    elif return_type == 'csv':
        epic.to_csv(CONFIG.file_path_epic_summary)
