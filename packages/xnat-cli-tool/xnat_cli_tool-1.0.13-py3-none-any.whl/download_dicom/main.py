import sys
from xnat import connect
import os
import shutil
import json

def copy_subdirs_to_output(input_dir, output_dir):
    for project_dir in os.listdir(input_dir):
        project_path = os.path.join(input_dir, project_dir)
        if os.path.isdir(project_path):
            for sub_dir in os.listdir(project_path):
                sub_dir_path = os.path.join(project_path, sub_dir)
                if os.path.isdir(sub_dir_path):
                    dest_path = os.path.join(output_dir, project_dir, sub_dir)
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.copytree(sub_dir_path, dest_path, dirs_exist_ok=True)
                    print(f"Copied {sub_dir_path} to {dest_path}")

def move_files(source_dir, destination_dir):
    """
    Moves files from the source directory to the destination directory.
    """
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file_path = os.path.join(root, file)

            if os.path.isfile(source_file_path):
                destination_file_path = os.path.join(destination_dir, file)
                shutil.move(source_file_path, destination_file_path)

def load_config():
    """
    Loads the configuration from the config file.
    """
    config_file = os.path.expanduser('~/.config/xnat_cli/config.json')
    
    if not os.path.exists(config_file):
        sys.exit('Config file not found. Please create a config file at ~/.config/xnat_cli/config.json')

    with open(config_file, 'r') as f:
        return json.load(f)

def setup_directories(base_dir, project, subject, output_dir):
    """
    Sets up the input, output, and temporary directories.
    """
    head_path = os.path.join(base_dir, 'input', project, subject)
    os.makedirs(head_path, exist_ok=True)

    if output_dir:
        output_path = os.path.join(output_dir, project)
    else:
        output_path = os.path.join(base_dir, 'output', project)
    os.makedirs(output_path, exist_ok=True)

    temp_dir = os.path.join(base_dir, 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    return head_path, output_path, temp_dir

def download_subject_data(session, subject, head_path, temp_dir):
    """
    Downloads the data for a single subject.
    """
    for experiment in subject.experiments.values():
        experiment_id = experiment.label
        experiment_path = os.path.join(head_path, experiment_id, 'SCANS')
        os.makedirs(experiment_path, exist_ok=True)


        for session_id, scan in experiment.scans.items():
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)

            for resource_name, resource in scan.resources.items():
                if resource.label == 'DICOM':
                    try:
                        resource.download_dir(temp_dir)
                        scan_dir = os.path.join(experiment_path, scan.id, resource.label)
                        os.makedirs(scan_dir, exist_ok=True)

                        move_files(temp_dir, scan_dir)
                        print(f"Resource {resource_name} for session {session_id} downloaded to {scan_dir}")
                    except Exception as e:
                        print(f'Error downloading resource {resource_name} for session {session_id}: {e}')



def download_data(output_dir=None, subjects=None, project=None):
    """
    Connects to the XNAT server and downloads the data for the specified subjects or project.
    
    Args:
        output_dir (str): Directory to save the downloaded data.
        subjects (list): List of subject labels to download.
        project (str): Project ID to download data from.
    """
    print(output_dir, subjects, project)
    config_data = load_config()
    server = config_data['server']
    username = config_data['username']
    secret = config_data['secret']

    with connect(server, username, secret) as session:
        subject_data = session.classes.SubjectData
        target_subjects = []

        if project:
            target_project = session.projects.get(project)
            if not target_project:
                sys.exit(f"No project found with ID '{project}'")
            if subjects:
                for sub in subjects:
                    cursor = next((subject for subject in target_project.subjects.values() if subject.label == sub), None)
                    if cursor:
                        target_subjects.append(cursor)
                    else:
                        print(f"No subjects found for label '{sub}'")
            else:
                target_subjects = target_project.subjects.values()
        elif subjects:
            for sub in subjects:
                cursor = subject_data.query().filter(subject_data.label.like(f'{sub}')).all()
                if not cursor:
                    print(f"No subjects found for label '{sub}'")
                    continue
                target_subjects.extend(cursor)
        else:
            sys.exit('Please provide a subject label, a project name, or both for data retrieval.')

        base_dir = os.getcwd()
        for subject in target_subjects:
            head_path,output_path, temp_dir = setup_directories(base_dir, subject.project, subject.label, output_dir)
            download_subject_data(session, subject, head_path, temp_dir)

        copy_subdirs_to_output('./input', output_dir)

            
  
                
        # Clean up directories
        shutil.rmtree(os.path.join(base_dir, 'input'))
        shutil.rmtree(os.path.join(base_dir, 'temp'))

def download_dicom_script(args):
    """
    Script entry point for downloading DICOM data based on provided arguments.
    """
    if not args.output or (not args.subject_label and not args.project_id):
        sys.exit('Please provide a subject label, a project name, or both for data retrieval.')

    base_dir = os.getcwd()
    shutil.rmtree(os.path.join(base_dir, 'input'), ignore_errors=True)
    shutil.rmtree(os.path.join(base_dir, 'temp'), ignore_errors=True)
    os.makedirs(os.path.join(base_dir, 'input'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'temp'), exist_ok=True)

    download_data(args.output, args.subject_label, args.project_id)
