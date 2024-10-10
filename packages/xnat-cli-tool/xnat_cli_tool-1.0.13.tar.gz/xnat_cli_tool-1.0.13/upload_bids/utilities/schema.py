import os 

def explore_directory_structure(root_path):
    """
    Traverses the directory structure starting from 'root_path', filters directories based on conditions,
    and retrieves information about subjects and their sessions.

    Args:
    - root_path (str): The root path from which the directory traversal begins.

    Returns:
    - list of dicts: Information about subjects and their sessions. Each dictionary contains:
        - 'subject_name': Name of the subject directory.
        - 'subject_path': Full path to the subject directory.
        - 'sessions': List of dictionaries containing session information.
                      Each session dictionary contains 'name' and 'path'.
        - 'is_single_ses': Indicates if the subject has a single session (True/False).
    """
    subjects = []

    for dir_path, dir_names, _ in os.walk(root_path):
        
        for dir_name in dir_names:
            if dir_name.startswith('sub-') and '_' not in dir_name and not any(item in dir_path for item in ['tmp', 'sourcedata', 'code']):
                subject_path = os.path.join(dir_path, dir_name)
                subject_info = {'subject_name': dir_name, 'subject_path': subject_path, 'sessions': [], 'is_single_ses': False}

                ses_dirs = [ses for ses in os.listdir(subject_path) if ses.startswith('ses-') and os.path.isdir(os.path.join(subject_path, ses))]
                if ses_dirs:
                    subject_info['sessions'] = [{'name': ses, 'path': os.path.join(subject_path, ses)} for ses in ses_dirs]
                else:
                    subject_info['is_single_ses'] = True
                    subject_info['sessions'].append({'name': 'Single Session', 'path': subject_path})

                subjects.append(subject_info)
    return subjects
