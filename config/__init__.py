class CONFIG:
    file_path_exported_defects       = 'temp/defects.xlsx'
    file_path_exported_user_stories  = 'temp/user_stories.xlsx'
    file_path_sev_vs_status          = 'temp/sev_vs_status.csv'

class DEFECTS:
    class PARAMETER_MAPPING:
        id                      = 'defect_id'
        title                   = 'title'
        severity                = 'severity'
        status                  = 'status'
        discovery_method        = 'discovery_method'
        disposition_type        = 'disposition_type'
        times_failed_verified   = 'fail_verify_count'
        created_date            = 'created'
        moved_to_verify_date    = 'to_verify'
        closed_date             = 'to_close'
        other_links             = 'link'

    class STATUS:
        submit      = 'submit'
        analyze     = 'analyze'
        verify      = 'verify'
        closed      = 'close'

    class SEVERITY:
        Sev_1 = 1
        Sev_2 = 2
        Sev_3 = 3

class USER_STORIES:
    class PARAMETER_MAPPING:
        id                      = 'id'
        title                   = 'summary'
        status                  = 'status'
        story_points            = 'story_points'
        linked_epic             = 'epic'
        linked_release_version  = 'version'
    
    class STATUS:
        defined         = 'defined'
        in_progress     = 'in progress'
        completed       = 'completed'
        accepted        = 'accepted'
