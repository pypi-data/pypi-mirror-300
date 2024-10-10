import json 
import os 

def logout():
    config_file = os.path.expanduser('~/.config/xnat_cli/config.json')

    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)
    except FileNotFoundError:
        print("No configuration file found.")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format in the configuration file.")
        return

    if 'username' in config_data:
        del config_data['username']
    if 'secret' in config_data:
        del config_data['secret']

    with open(config_file, 'w') as file:
        json.dump(config_data, file)

    print("Logged out successfully.")