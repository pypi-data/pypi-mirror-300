import os 
import sys 
import glob
from .scan import create_new_scan

def deleteConfigFile():
    """
    A function that deletes a configuration file if it exists.

    Args:
    - None

    Returns:
    - bool: True if the configuration file was deleted, False otherwise.
    """

    # Check if the configuration file exists
    if os.path.exists('config.json'):
        # If it exists, delete it
        os.remove('config.json')
        print('Config file has been deleted.')
        return True

    # If the configuration file doesn't exist, return False
    return False

def find_session_folders(root_folder):
    """
    A function that finds all session folders in a root directory.

    Args:
    - root_folder (str): The path to the root directory.

    Returns:
    - list: A list of session folder names.
    """

    # Create an empty list to store session folder names
    sessions = []

    # Iterate through all subdirectories in the root directory
    folders = [foldername for foldername in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, foldername))]
    for subfolder in folders:
        # If the subdirectory name begins with "sub-", add it to the list of session folders
        if subfolder.startswith('sub-'):
            sessions.append(subfolder)

    return sessions

def _validate_bids(root_path):
    """
    A function that checks if a directory conforms to the BIDS schema.

    Args:
    - root_path (str): The path to the directory to be validated.

    Returns:
    - bool: True if the directory conforms to the BIDS schema, False otherwise.
    """

    # List all subdirectories in the root directory
    required_directories = ['dwi', 'fmap', 'anat', 'func', 'perf']

    # Check if any of the expected subdirectories (dwi, fmap, anat ,func, perf) are present in the root directory
    for dirpath, dirnames, scans in os.walk(root_path):
        if not all(subdir in required_directories for subdir in dirnames):
            return False
    return True


def validate_input_data(root_path):
    """
    A function that validates input data against the BIDS schema.

    Args:
    - root_path (str): The path to the root directory of the input data.

    Returns:
    - None
    """

    # Check if there are any session folders in the root directory
    session_folders = find_session_folders(root_path)

    if not session_folders:
        # If there are no session folders, validate the root directory
        if not _validate_bids(root_path):
            print(f"Invalid schema found in {root_path}")
            sys.exit(1)
    else:
        # If there are session folders, iterate through them and validate each one
        for session in session_folders:
            if not _validate_bids(f"{root_path}/{session}"):
                print(f"Invalid schema found in {root_path}/{session}")
                sys.exit(1)

def _find_files_by_name(root_path, file_name):
    file_pattern = os.path.join(root_path, file_name + '.*')
    return glob.glob(file_pattern)


def upload_BIDS(experiment, session_path):
    """
    A function that uploads BIDS-formatted data to an experiment.

    Args:
    - experiment (str): The name of the experiment to which the data will be uploaded.
    - session_path (str): The path to the session directory containing the BIDS-formatted data.

    Returns:
    - None
    """

    # Iterate through all files in the session directory
    for root, directories, files in os.walk(session_path):
        for scan in files:

            # Check if the file is a JSON file and if a corresponding NIfTI file exists
            if (scan.endswith('.json')) and (os.path.exists(os.path.join(root, f'{os.path.splitext(scan)[0]}.nii')) or os.path.exists(os.path.join(root, f'{os.path.splitext(scan)[0]}.nii.gz'))):
                
                # Call the createNewScan function with the experiment name, directory path, and scan
                files = _find_files_by_name(root,scan.split('.')[0])
                if len(files) >= 2:
                    create_new_scan(experiment, files, scan)
                else:
                    print(f'An error occurred while attempting to upload this data. {files}')

