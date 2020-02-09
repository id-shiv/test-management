import pandas as pd
import matplotlib.pyplot as plt

from config import CONFIG, PARAMETER_MAPPING, STATUS, SEVERITY


def clean(defects):
    ## Get the defects data ready for processing
    # Rename the column names to standarize (based on PARAMETER MAPPING)
    defects = defects.rename(columns= dict((v,k) for k, v in PARAMETER_MAPPING.items()))

    # Rename status to standardize the names (based on STATUS)
    defects = defects.replace(dict((v,k) for k, v in STATUS.items()))

    # Rename severity to standardize the names (based on STATUS)
    defects = defects.replace(dict((v,k) for k, v in SEVERITY.items()))

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
    table_status_vs_severity = defects.pivot(index='status', columns='severity', values='count').fillna(0)

    # Remove row with status 'closed' to calculate open defects
    closed = table_status_vs_severity.loc['closed']
    table_status_vs_severity = table_status_vs_severity.drop('closed', axis=0)
    # print(table_status_vs_severity)

    # Total open defects 
    table_status_vs_severity.loc['open defects', :] = table_status_vs_severity.sum(axis=0)
    # print(table_status_vs_severity)

    # Insert closed defects count
    table_status_vs_severity = table_status_vs_severity.append(closed)
    # print(table_status_vs_severity)

    # Total per severity
    table_status_vs_severity.loc[:, 'total'] = table_status_vs_severity.sum(axis=1)
    # print(table_status_vs_severity)

    # Total open defects 
    table_status_vs_severity.loc['total', :] = table_status_vs_severity.sum(axis=0)
    # print(table_status_vs_severity)

    # Add columns to have at least one sample with all levels of severity
    if not 'Sev-1' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev-1'] = 0
    if not 'Sev-2' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev-2'] = 0
    if not 'Sev-3' in table_status_vs_severity.columns:
        table_status_vs_severity['Sev-3'] = 0

    # Insert the status column
    table_status_vs_severity['status'] = table_status_vs_severity.index
    # print(table_status_vs_severity)

    # Add rows to have at least one sample with all levels of status
    if not any(table_status_vs_severity['status'].str.contains('submit')):
        table_status_vs_severity = table_status_vs_severity.append({'status': 'submit'}, ignore_index=True)
    if not any(table_status_vs_severity['status'].str.contains('analyze')):
        table_status_vs_severity = table_status_vs_severity.append({'status': 'anlayze'}, ignore_index=True)
    if not any(table_status_vs_severity['status'].str.contains('verify')):
        table_status_vs_severity = table_status_vs_severity.append({'status': 'verify'}, ignore_index=True)
    if not any(table_status_vs_severity['status'].str.contains('closed')):
        table_status_vs_severity = table_status_vs_severity.append({'status': 'closed'}, ignore_index=True)
    table_status_vs_severity = table_status_vs_severity.fillna(0)

    # Re order the columns
    re_ordered_columns = ["status", 'Sev-1', 'Sev-2', 'Sev-3', "total"]
    table_status_vs_severity = table_status_vs_severity[re_ordered_columns]

    # Re order the rows
    status_order = ['submit', 'analyze', 'verify', 'open defects', 'closed', 'total']
    index_order = [table_status_vs_severity[table_status_vs_severity['status'] == status].index .values.astype(int)[0] for status in status_order]
    table_status_vs_severity = table_status_vs_severity.loc[index_order, :]

    # Convert all float values to int
    table_status_vs_severity[['Sev-1', 'Sev-2', 'Sev-3', 'total']] = table_status_vs_severity[['Sev-1', 'Sev-2', 'Sev-3', 'total']].astype('int32')

    if return_type == 'table':
        return table_status_vs_severity
    elif return_type == 'csv':
        table_status_vs_severity.to_csv(CONFIG.file_path_sev_vs_status, index=False)
