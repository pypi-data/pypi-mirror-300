import os


def create_new_scan(experiment, files, scan_name):
    '''
    Create a new scan within the given experiment.

    Parameters:
    experiment (pyxnat.core.resources.Experiment): The experiment object to create the scan within.
    root_path (str): The root path of the session folder.
    scan_name  (str): The name of the BIDS scan.

    Returns:
    The newly created scan object.
    '''
    
    # Extract scan id from filename
    scan_id = scan_name.split('.')[0]
    dirname = os.path.dirname(files[0])
    directory_name = os.path.basename(dirname)

    scan = experiment.scan(scan_id.split('_', 1)[1])
    # Create new scan if it doesn't exist in experiment
    if not scan.exists():
        scan.create()
        scan.attrs.set('type', directory_name)
        scan.attrs.set('series_description', scan_id)
        scan.attrs.set('quality', 'usable')

    # Create scan resource
    scan_resource = scan.resource('BIDS')
    
    for f in files:
        file_size = os.path.getsize(f)
        print(f'Uploading {os.path.basename(f)}: {file_size} bytes')
        scan_resource.file(os.path.basename(f)).insert(
                    f,
                    content=directory_name,
                    format='NIFTI',
                    tags='BIDS',
        )
