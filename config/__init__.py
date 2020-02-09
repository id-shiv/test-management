class CONFIG:
    file_path_exported_defects  = 'config/defects.xlsx'
    file_path_sev_vs_status     = 'temp/sev_vs_status.csv'

PARAMETER_MAPPING = {
    'id'                    : 'defect_id',
    'title'                 : 'title',
    'severity'              : 'severity',
    'status'                : 'status',
    'discovery_method'      : 'discovery_method',
    'disposition_type'      : 'disposition_type',
    'times_failed_verified' : 'fail_verify_count',
    'created_date'          : 'created',
    'moved_to_verify_date'  : 'to_verify',
    'closed_date'           : 'to_close',
    'other_links'           : 'link'
}

STATUS = {
    'submit'    : 'submit',
    'analyze'   : 'analyze',
    'verify'    : 'verify',
    'closed'    : 'close'
}

SEVERITY = {
    'Sev-1': 1,
    'Sev-2': 2,
    'Sev-3': 3
}
