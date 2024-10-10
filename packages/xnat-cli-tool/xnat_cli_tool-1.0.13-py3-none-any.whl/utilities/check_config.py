import os
import json

def check_config():
    config_file = os.path.expanduser('~/.config/xnat_cli/config.json')

    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            json.dump({}, file)

    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)
    except json.JSONDecodeError:
        config_data = {}

    required_keys = ['server', 'username', 'secret']
    missing_keys = [key for key in required_keys if key not in config_data or not config_data[key]]

    if missing_keys:
        print("\033[91m" + "Warning: Configuration for the CLI is incomplete or missing." + "\033[0m" + "\n")

