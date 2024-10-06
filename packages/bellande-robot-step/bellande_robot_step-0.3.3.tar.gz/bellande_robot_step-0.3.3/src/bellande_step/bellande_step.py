import subprocess
import argparse
import json
import os
import sys

def get_executable_path():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(application_path, 'Bellande_Step')

def run_bellande_step(coord1, coord2, limit, dimensions):
    executable_path = get_executable_path()
    passcode = "bellande_step_executable_access_key"

    # Convert string representations of coordinates to actual lists
    coord1_list = json.loads(coord1)
    coord2_list = json.loads(coord2)

    # Validate input
    if len(coord1_list) != dimensions or len(coord2_list) != dimensions:
        raise ValueError(f"Coordinates must have {dimensions} dimensions")

    # Prepare the command
    command = [
        executable_path,
        passcode,
        json.dumps(coord1_list),
        json.dumps(coord2_list),
        str(limit),
        str(dimensions)
    ]

    # Run the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Error output:", e.stderr)

def main():
    parser = argparse.ArgumentParser(description="Run Bellande Step executable")
    parser.add_argument("coord1", help="First coordinate as a JSON-formatted list")
    parser.add_argument("coord2", help="Second coordinate as a JSON-formatted list")
    parser.add_argument("limit", type=int, help="Limit for the algorithm")
    parser.add_argument("dimensions", type=int, help="Number of dimensions")
    
    args = parser.parse_args()

    run_bellande_step(
        args.coord1,
        args.coord2,
        args.limit,
        args.dimensions
    )

if __name__ == "__main__":
    main()
