import os
import signal
import sys

from .utilities import \
        XnatClient,\
        createExperiment,\
        existSignalHandler,\
        deleteConfigFile,\
        validate_input_data,\
        find_session_folders,\
        upload_BIDS,\
        explore_directory_structure
    


def upload_bids_script(args):
    signal.signal(signal.SIGINT, existSignalHandler)

    if not args.project_id or not args.input_path:
        print(args.project_id , args.input_path)
        print("Make sure you have entered the project id and exist directory path")
        sys.exit(1)

    if not os.path.exists(args.input_path):
        print("No directory found, Check your path")
        sys.exit(1)



    root_path = args.input_path
    project_label = args.project_id

    subject_label = os.path.basename(root_path)

    # List of subject if is exist or not 
    #subjects = find_session_folders(root_path)
    subjects = explore_directory_structure(root_path)

    try:
        connection = XnatClient()
        #validate_input_data(root_path)
        
    except KeyboardInterrupt:
        pass

    if connection.session.select.project(project_label).exists():
        project = connection.session.select.project(project_label)
        
        if subjects:
            print(f'The number of subjects found in the {root_path} = {len(subjects)}')

            for subject in subjects:
                s = project.subject(subject['subject_name'])

                if not s.exists():
                    s.create()
                    print(f"Creating a new subject with name {subject['subject_name']}")
                else:
                    print(f"Found a subject with name {subject['subject_name']}")

                for session in subject['sessions']:
                    if subject['is_single_ses'] == 'True':
                        exp = createExperiment(s,session['path'],f"{project_label}_{subject['subject_name']}_ses-01")
                    else:
                        exp = createExperiment(s,session['path'],f"{project_label}_{subject['subject_name']}_{session['name']}")

                    upload_BIDS(exp,session['path'])

        else:
            print(f'No subject found!')

    else:
        print('Project dose not exist')

    connection.disconnect()
