import json
import os
import getpass
import sys
from pyxnat import Interface
from .fileServices import deleteConfigFile

def Core(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@Core
class XnatClient:

    def __init__(self):
        '''
        Initializes a new instance of the XnatClient class.

        Args:
        - None

        Returns:
        - None
        '''

        self.is_connect = False
        # Establish a new session and assign it to the 'session' attribute
        self.session = self._establish_session()

    def _establish_session(self):
        '''
        _establish_session a new PyXNAT session with user-provided credentials.
        If configuration file exists and is valid, use it as default.
        '''

        config_file = os.path.expanduser('~/.config/xnat_cli/config.json')

        if not os.path.exists(config_file):
            sys.exit("No config file found. Please run 'xnat login' to create a new config file.")

        with open(config_file, 'r') as f:
            config_data = json.load(f)

        required_keys = ['server', 'username', 'secret']
        missing_keys = [key for key in required_keys if key not in config_data or not config_data[key]]

        if missing_keys:
            sys.exit("Warning: Configuration for the CLI is incomplete or missing. make sure you login first")


        session = Interface(server=config_data['server'], user= config_data['username'], password=config_data['secret'])

        if session._get_entry_point() != '/data':
            sys.exit('Invalid credentials. Please run "xnat login" to create a new config file.')
            
        self.is_connect = True
        return session
    
    def disconnect(self):
        '''
        End the session in the XNAT server.

        Args:
        - None

        Returns:
        - None
        '''
        try:
            # Disconnect the session and set the 'is_connect' flag to False
            self.session.disconnect()
            self.is_connect = False
            sys.exit(0)
        except:
            pass
