from .fileServices import deleteConfigFile
from .core import XnatClient


def existSignalHandler(sig, frame):
    '''
    Handles signals to exit the program gracefully.

    Args:
    - sig (int): The signal number.
    - frame (frame): The current stack frame.

    Returns:
    - None
    '''

    try:
        # get XnatClient session and disconnect if connected
        session = XnatClient()
        if session.is_connect:
            XnatClient.disconnect()
    except:
        pass    
    exit(0)