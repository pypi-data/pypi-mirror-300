import os
import pydicom
import xnat
import re
import shutil
import zipfile
import sys
import json

temp_dir = 'temp_dicom_files'


def get_next_ses_number(file_path):
    # Get the session directory (parent directory of the scan directory)
    root = os.path.dirname(os.path.dirname(file_path))
    session_dir = os.path.dirname(os.path.dirname(root))

    # Check if the session directory name starts with 'anat'
    session_dir_name = os.path.basename(session_dir)

    if session_dir_name.startswith("ses"):
        # Extract the number after 'anat' if it exists
        number_match = re.search(r'ses_(\d+)', session_dir_name)
       
        if number_match:
            number = int(number_match.group(1))
            print(number)
            # Format the number with two decimal places
            return f"ses-{number:02d}"
        else:
            # If 'anat' is found without a number, return 'ses-01'
            return "ses-01"

    # If the directory name does not start with 'anat', return 'ses-01' by default
    return "ses-01"


def process_dicom_file(file_path, project_name):
    pattern = r'fw:\/\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)'

    with pydicom.dcmread(file_path) as dcm:
        study_description = dcm.StudyDescription
        matches = re.match(pattern, study_description)
        group_3 = (matches.group(3)) if matches and matches.group(3).startswith('S') else str(dcm.PatientName)
        group_4 = get_next_ses_number(file_path=file_path)
        
        if not group_3.startswith('S'):
            with open('log.txt', 'a') as log_file:
                log_file.write(f'Skipped: {file_path}\n')
            return None

        group_3 = group_3.replace(' ', '_') if ' ' in group_3 else group_3

        dcm.StudyDescription = f'xnat://{project_name}/{group_3}/{group_4}'
        print(file_path,':',group_4)

        subject_name = group_3
        session_name = group_4
        dcm.save_as(file_path)

        # temp_file_path = os.path.join(temp_dir, subject_name, session_name, os.path.basename(file_path))
        # os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        # dcm.save_as(temp_file_path)
        return True

def process_directory(directory_path, project_name):
    dicom_files = []
    
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".dcm"):
                dicom_files.append(os.path.join(root, file_name))
    
    processed_paths = []
    for file_path in dicom_files:
        new_path = process_dicom_file(file_path, project_name)
        processed_paths.append(new_path)
    
    return True

def upload_to_xnat(server, username, password, files, single=False):
    session = xnat.connect(server=server, user=username, password=password)
    for file_path in files:
        print(f"Uploading {file_path}.zip to XNAT")
        if not single:
            session.services.import_(os.path.join(f'{file_path}.zip'), destination='/prearchive')
        else:
            session.services.import_(file_path, destination='/prearchive')
    session.disconnect()

def create_zip(subject_name):
    subject_dir = os.path.join(subject_name)

    # Compress the session directory into a zip file
    zip_path = os.path.join(f'{subject_name}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(subject_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), subject_dir))

    return zip_path

def upload_dicom_script(args):

    if not args.input_path or not args.project_name:
        print("Invalid input. Please provide a valid DICOM file path or directory path and project name.")
        sys.exit(1)

    input_path = args.input_path
    project_name = args.project_name

    config_file = os.path.expanduser('~/.config/xnat_cli/config.json')
    
    with open(config_file, 'r') as f:
        config_data = json.load(f)
        
    server = config_data['server']
    username = config_data['username']
    secret = config_data['secret']



    if not os.path.exists(input_path):
        print("No directory found, Check your input path")
        sys.exit(1)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if os.path.isfile(input_path) and input_path.endswith(".dcm"):
        processed_path = process_dicom_file(input_path, project_name)
        upload_to_xnat(server, username, secret,[processed_path],True)
        shutil.rmtree(temp_dir)

    elif os.path.isdir(input_path):
        subjects_dirs = [f.path for f in os.scandir(f'{input_path}') if f.is_dir() and f.name.startswith('Subject') or f.name.startswith('subject')]
        if subjects_dirs:
            for subject in subjects_dirs:
                print(f'{subject}')
                _ = process_directory(subject, project_name)        
                # sub_directories = [f.path for f in os.scandir(temp_dir) if f.is_dir() and f.name.startswith('Subject_') or f.name.startswith('subject_')]
                # compressed_paths=[]
                # for directory in sub_directories:
                #     zip_path = create_zip(directory)
                #     compressed_paths.append(directory)
                
                # upload_to_xnat(server, username, secret, compressed_paths)
                #shutil.rmtree(temp_dir)
        else:
            _ = process_directory(input_path, project_name)        
            sub_directories = [f.path for f in os.scandir(temp_dir) if f.is_dir() and f.name.startswith('S')]
            compressed_paths=[]

            # for directory in sub_directories:
            #     zip_path = create_zip(directory)
            #     compressed_paths.append(directory)

            # upload_to_xnat(server, username, secret, compressed_paths) 
            # shutil.rmtree(temp_dir) 

    else:
        print("Invalid input. Please provide a valid DICOM file path or directory path.")
        shutil.rmtree(temp_dir)
        sys.exit(1)

    try:
        shutil.rmtree(temp_dir) 
    except:
        pass