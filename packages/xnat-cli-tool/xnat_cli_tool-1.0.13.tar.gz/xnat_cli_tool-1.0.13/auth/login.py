import json
import sys
import os
from xnat import connect

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input.strip() or default_value

def login(args):
    if not args.username or not args.secret:
        print("Please provide username and secret")
        sys.exit(1)
        
    username = args.username
    secret = args.secret

    config_dir = os.path.join(os.path.expanduser('~/.config'), 'xnat_cli')
    config_file = os.path.join(config_dir, 'config.json')

    # Create the directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    config_data = {}

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as file:
                existing_data = json.load(file)
                config_data.update(existing_data)
        except FileNotFoundError:
            print("Config file not found. A new one will be created with default values.")
        except json.JSONDecodeError:
            print("Warning: Config file is corrupt. It will be overwritten.")
    else:
        print("Config file not found. A new one will be created with default values.")
        
    # Ask user for the server if it's not already in the config file
    if 'server' not in config_data:
        default_server = 'http://10.230.12.52'
        config_data['server'] = get_user_input("Enter the XNAT server URL", default_server)

    server = config_data['server']

    try:
        with connect(server, username, secret) as session:
            try:
                config_data.update({'username': username, 'secret': secret, "valid": True})

                with open(config_file, 'w') as file:
                    json.dump(config_data, file, indent=4)

                print(f"Logged in successfully with username: {username}")
            except Exception as e:
                print(f"Error saving credentials to config file: {e}")
                sys.exit(1)
    except Exception as e:
        print(f"Failed to login. Please check your username or secret. Error: {e}")
        sys.exit(1)
