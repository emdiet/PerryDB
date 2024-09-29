import argparse
import os
import sys
import json
import math

# Constant for the required filesystem version
FS_VERSION = 1.2

# Function to handle argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Start a file synchronization server.")
    parser.add_argument(
        "-d", "--directory",
        type=str,
        required=True,
        help="The starting directory to manage."
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        required=True,
        help="Port to listen for incoming requests."
    )
    parser.add_argument(
        "-i", "--initialize",
        action="store_true",
        help="Initialize the directory with the required structure."
    )
    return parser.parse_args()

# Function to ensure the directory structure and configuration are correct
def check_directory(directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Error: The specified directory '{directory}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    # Check for perryconf.json file
    config_path = os.path.join(directory, 'perryconf.json')
    if not os.path.exists(config_path):
        print(f"Error: The configuration file 'perryconf.json' is missing in {directory}.")
        sys.exit(1)

    # Check for WAL and STORE directories
    wal_directory = os.path.join(directory, 'WAL')
    store_directory = os.path.join(directory, 'STORE')

    if not os.path.exists(wal_directory):
        print(f"Error: The 'WAL' directory is missing in {directory}.")
        sys.exit(1)
    
    if not os.path.exists(store_directory):
        print(f"Error: The 'STORE' directory is missing in {directory}.")
        sys.exit(1)

    # Validate the perryconf.json file
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except Exception as e:
        print(f"Error: Failed to read 'perryconf.json'. {e}")
        sys.exit(1)

    # Ensure 'FS_VERSION' exists and is valid
    if 'FS_VERSION' not in config:
        print("Error: 'FS_VERSION' property is missing in 'perryconf.json'.")
        sys.exit(1)

    fs_version = config['FS_VERSION']
    if not isinstance(fs_version, (int, float)):
        print("Error: 'FS_VERSION' in 'perryconf.json' must be a number.")
        sys.exit(1)

    # Check that FS_VERSION is within the required range
    if not (FS_VERSION <= fs_version < math.ceil(FS_VERSION)):
        print(f"Error: 'FS_VERSION' ({fs_version}) is incompatible. Expected >= {FS_VERSION} and < {math.ceil(FS_VERSION)}.")
        sys.exit(1)

    print(f"Directory check passed. FS_VERSION: {fs_version}, WAL and STORE directories found.")

# Function to initialize the directory if needed
def initialize_directory(directory):
    print(f"Initializing directory structure in {directory}...")
    
    # Create the WAL and STORE directories if they don't exist
    wal_directory = os.path.join(directory, 'WAL')
    store_directory = os.path.join(directory, 'STORE')
    
    os.makedirs(wal_directory, exist_ok=True)
    os.makedirs(store_directory, exist_ok=True)
    
    # Create or validate the perryconf.json file
    config_path = os.path.join(directory, 'perryconf.json')
    
    if not os.path.exists(config_path):
        config = {
            "FS_VERSION": FS_VERSION
        }
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        print(f"'perryconf.json' created with FS_VERSION {FS_VERSION}.")
    else:
        print(f"'perryconf.json' already exists. No changes made.")
    
    print(f"Directory initialized successfully.")

# Main function to start the server
def start_server(directory, port):
    print(f"Starting server with directory: {directory} on port: {port}")
    # Placeholder for starting the actual server logic
    # This will eventually handle pub/sub, WAL, file syncing, etc.
    # You could use something like FastAPI or Flask to handle HTTP requests

if __name__ == "__main__":
    args = parse_arguments()

    # Initialize the directory if needed
    if args.initialize:
        initialize_directory(args.directory)
    
    # Ensure the starting directory is valid and meets the requirements
    check_directory(args.directory)
    
    # Start the server
    start_server(args.directory, args.port)
