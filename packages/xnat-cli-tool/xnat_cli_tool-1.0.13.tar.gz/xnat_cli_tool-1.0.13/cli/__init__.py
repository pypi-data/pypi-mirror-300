import argparse
from utilities.check_config import check_config
from auth.login import login
from auth.logout import logout
from download_bids.main import download_bids_script
from download_dicom.main import download_dicom_script
from upload_bids.main import upload_bids_script
from upload_dicom.main import upload_dicom_script

VERSION = "1.0.10"
HELP_EMAIL = "nyuad.xnat@nyu.edu"

def cli():
    print(f"\033[93mThis is a Beta version of the XNAT CLI Tool. For assistance, please contact: {HELP_EMAIL} \033[0m")

    parser = argparse.ArgumentParser(description="XNAT CLI Tool")
    parser.add_argument('--version', action='version', version=f'XNAT CLI V{VERSION}')
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Login command
    login_parser = subparsers.add_parser('login', help='Login to XNAT')
    login_parser.add_argument('username', help='Username for XNAT')
    login_parser.add_argument('secret', help='Secret key for XNAT')
    login_parser.set_defaults(func=login)

    # Logout command
    logout_parser = subparsers.add_parser("logout", help="Logout from XNAT")
    logout_parser.set_defaults(func=logout)

    # Download BIDS command
    parser_download_bids = subparsers.add_parser("download_bids", help="Download BIDS data")
    # group = parser_download_bids.add_mutually_exclusive_group(required=True)
    parser_download_bids.add_argument("-s", "--subject_label",nargs='+',help="Subject label for downloading data. If specified, the tool will download data for this subject. e.g., Subject_0001")
    parser_download_bids.add_argument("-p", "--project_id", help="Project ID for downloading data. If specified, the tool will download data for all subjects in this project. e.g., Project_01")
    parser_download_bids.add_argument("-o", "--output", required=True, help="Output directory for saving the data")
    parser_download_bids.set_defaults(func=download_bids_script)
    parser_download_bids.usage = '''
    Example usage:
    To download \033[93mBIDS\033[0m data for a specific subject:
        xnat download_bids -s SUBJECT_LABEL -o /path/to/output_directory

    To download \033[93mBIDS\033[0m data for all subjects in a project:
        xnat download_bids -p PROJECT_ID -o /path/to/output_directory
    '''

     # Download DICOM command
    parser_download_dicom = subparsers.add_parser("download_dicom", help="Download DICOM data")
    parser_download_dicom.add_argument("-s", "--subject_label", nargs='+', help="Subject label for downloading data. If specified, the tool will download data for this subject. e.g., Subject_0001")
    parser_download_dicom.add_argument("-p", "--project_id", help="Project ID for downloading data. If specified, the tool will download data for all subjects in this project. e.g., Project_01")
    parser_download_dicom.add_argument("-o", "--output", required=True, help="Output directory for saving the data")
    parser_download_dicom.set_defaults(func=download_dicom_script)
    parser_download_dicom.usage = '''
    Example usage:
    To download \033[93mDICOM\033[0m data for a specific subject:
        xnat download_dicom -s SUBJECT_LABEL -o /path/to/output_directory

    To download \033[93mDICOM\033[0m data for all subjects in a project:
        xnat download_dicom -p PROJECT_ID -o /path/to/output_directory
    '''

    # Upload BIDS command
    parser_upload_bids = subparsers.add_parser("upload_bids", help="Upload BIDS data")
    parser_upload_bids.add_argument("-i", "--input_path", help="Directory path containing the data to upload", required=True)
    parser_upload_bids.add_argument("-p", "--project_id", help="Project ID to upload data to", required=True)
    parser_upload_bids.set_defaults(func=upload_bids_script)
    parser_upload_bids.usage = '''
    Example usage:
    To upload BIDS data to a project:
        xnat upload_bids -i /path/to/directory -p PROJECT_ID
    '''

    # Upload DICOM command
    parser_upload_dicom = subparsers.add_parser("upload_dicom", help="Upload DICOM data")
    parser_upload_dicom.add_argument('input_path', help='Path to the DICOM files')
    parser_upload_dicom.add_argument('project_name', help='Project ID to upload data to')
    parser_upload_dicom.set_defaults(func=upload_dicom_script)
    parser_upload_dicom.usage = '''
    Example usage:
    To upload DICOM data to a project:
        xnat upload_dicom /path/to/dicom_files PROJECT_ID  
    '''

    # Help command
    help_parser = subparsers.add_parser("help", help="Get help information")
    help_parser.set_defaults(func=lambda args: show_help(parser))

    args = parser.parse_args()

    if args.command != 'login':
        check_config()

    command_map = {
        "download_bids": download_bids_script,
        "download_dicom": download_dicom_script,
        "upload_bids": upload_bids_script,
        "upload_dicom": upload_dicom_script,
        "login": login,
        "logout": logout
    }

    if args.command in command_map:
        command_map[args.command](args)
    elif args.command == "help":
        show_help(parser)
    else:
        parser.print_help()

def show_help(parser):
    print(f"For assistance, please contact: {HELP_EMAIL}")
    parser.print_help()

if __name__ == '__main__':
    cli()
