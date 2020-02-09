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
