import pandas as pd
import matplotlib.pyplot as plt

from config import CONFIG, DEFECTS


def clean(defects):
    ## Get the defects data ready for processing
    # Rename the column names to standarize (based on PARAMETER MAPPING)
    mapping = {value: key for key, value in DEFECTS.PARAMETER_MAPPING.__dict__.items() if not key.startswith('__') and not callable(key)}
    defects = defects.rename(columns = mapping)

    # Rename status to standardize the names (based on STATUS)
    mapping = {value: key for key, value in DEFECTS.STATUS.__dict__.items() if not key.startswith('__') and not callable(key)}
    defects = defects.replace(mapping)

    # Rename severity to standardize the names (based on STATUS)
    mapping = {value: key for key, value in DEFECTS.SEVERITY.__dict__.items() if not key.startswith('__') and not callable(key)}
    defects = defects.replace(mapping)

    defects['count'] = 1 # add a column 'count' to get the count while deriving charts

    defects = defects.fillna(0) # fill empty cell values with 0

    ## View the data before processing
    # print(defects)
    # print(defects.shape)
    # print(defects.describe())
    # print(defects.info())
    return defects

def get_status_vs_severity(defects, return_type='csv'):
    ## Get reports

    # Get status vs severity pivot table
    table_status_vs_severity = defects.pivot(index=DEFECTS.PARAMETER_MAPPING.status, 
                                             columns=DEFECTS.PARAMETER_MAPPING.severity, 
                                             values='count').fillna(0)

    # Remove row with status 'closed' to calculate open defects
    closed = table_status_vs_severity.loc['closed']
    table_status_vs_severity = table_status_vs_severity.drop('closed', axis=0)
    # print(table_status_vs_severity)

    # Total open defects 
    table_status_vs_severity.loc['Open Defects', :] = table_status_vs_severity.sum(axis=0)
    # print(table_status_vs_severity)

    # Insert closed defects count
    table_status_vs_severity = table_status_vs_severity.append(closed)
    # print(table_status_vs_severity)

    # Total per severity
    table_status_vs_severity.loc[:, 'Total'] = table_status_vs_severity.sum(axis=1)
    # print(table_status_vs_severity)

    # Total open defects 
    table_status_vs_severity.loc['Total', :] = table_status_vs_severity.sum(axis=0)
    # print(table_status_vs_severity)

    # Add columns to have at least one sample with all levels of severity
    if not 'Sev_1' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev_1'] = 0
    if not 'Sev_2' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev_2'] = 0
    if not 'Sev_3' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev_3'] = 0

    # Insert the status column
    table_status_vs_severity['Status'] = table_status_vs_severity.index
    # print(table_status_vs_severity)

    # Add rows to have at least one sample with all levels of status
    if not any(table_status_vs_severity['Status'].str.contains('submit')):
        table_status_vs_severity = table_status_vs_severity.append({'Status': 'submit'}, ignore_index=True)
    if not any(table_status_vs_severity['Status'].str.contains('analyze')):
        table_status_vs_severity = table_status_vs_severity.append({'Status': 'analyze'}, ignore_index=True)
    if not any(table_status_vs_severity['Status'].str.contains('verify')):
        table_status_vs_severity = table_status_vs_severity.append({'Status': 'verify'}, ignore_index=True)
    if not any(table_status_vs_severity['Status'].str.contains('closed')):
        table_status_vs_severity = table_status_vs_severity.append({'Status': 'closed'}, ignore_index=True)
    
    table_status_vs_severity = table_status_vs_severity.fillna(0)

    # Re order the columns
    re_ordered_columns = ['Status', 
                         'Sev_1', 
                         'Sev_2',
                         'Sev_3',
                         "Total"]
    table_status_vs_severity = table_status_vs_severity[re_ordered_columns]

    # Re order the rows
    status_order = ['submit', 
                    'analyze', 
                    'verify',
                    'Open Defects', 
                    'closed', 
                    'Total']
    index_order = [table_status_vs_severity[table_status_vs_severity['Status'] == status].index .values.astype(int)[0] for status in status_order]
    table_status_vs_severity = table_status_vs_severity.loc[index_order, :]

    # Convert all float values to int
    columns_to_convert = ['Sev_1', 
                         'Sev_2',
                         'Sev_3',
                         'Total']
    table_status_vs_severity[columns_to_convert] = table_status_vs_severity[columns_to_convert].astype('int32')

    if return_type == 'table':
        return table_status_vs_severity
    elif return_type == 'csv':
        table_status_vs_severity.to_csv(CONFIG.file_path_sev_vs_status, index=False)
