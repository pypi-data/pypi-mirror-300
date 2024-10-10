import time
import os
import sys

def createExperiment(subject, session_path, session_name):
    '''
    Create a new experiment with the given subject object.

    Args:
    - subject (pyxnat.core.resources.Subject): The subject to create the experiment for.
    - session_path (str): The path to the session directory.
    -session_name (str): The session name

    Returns:
    - pyxnat.core.resources.Experiment: The newly created experiment object.
    '''

    # Get the creation time of the session directory and extract the date and folder name
    creation_time = os.path.getctime(session_path)
    date = time.strftime('%Y-%m-%d', time.localtime(creation_time))

    # Construct the experiment label and create a new experiment object
    # experiment_label = f"{folder_name}-{date}-MR"
    experiment_label = f"{session_name}"
    experiment = subject.experiment(experiment_label)

    # Check if the experiment already exists
    if not experiment.exists():
        # If it doesn't exist, create it and set the date attribute
        print(f'Creating a new experiment with name {experiment_label}')
        experiment.create()
        experiment.attrs.set('date', date)
    else:
        # If it already exists, print a message indicating that it was found
        print(f'Found experiment with name {experiment_label}')
        sys.exit(0)

    return experiment



