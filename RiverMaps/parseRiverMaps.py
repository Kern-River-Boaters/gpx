# Copyright (c) 2026 Jose Luis Pino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Import necessary libraries
import gpxpy
import gpxpy.gpx
import sys
from pathlib import Path
import re

# Define a class to handle writing waypoints to GPX files
class GarminGpxFileWriter:
    def __init__(self, gpx_file_name, waypoint_type):
        """
        Initialize the GarminGpxFileWriter object.

        Args:
            gpx_file_name (str): The name of the GPX file.
            waypoint_type (str): The type of waypoints to add.
        """
        # Store the input parameters
        self.gpx_file_name = gpx_file_name
        self.waypoint_type = waypoint_type
        # Initialize counters and data structures
        self.file_index = 1
        self.waypoint_index = 0
        self.gpx = gpxpy.gpx.GPX()
        # Extract the river name from the file name
        self.riverName = Path(gpx_file_name).stem
        
    def add_waypoint(self, waypoint):
        """
        Add a waypoint to the GPX file and handle chunking limits.

        Args:
            waypoint (gpxpy.gpx.GPXWaypoint): The waypoint to add.
        """
        # Clear proprietary Garmin extensions to keep the file clean
        waypoint.extensions.clear()
        
        # Add the waypoint to the GPX object and increment the index
        self.gpx.waypoints.append(waypoint)
        self.waypoint_index += 1

        # If we've reached the maximum number of waypoints per file (99), write it out
        if self.waypoint_index == 99:
            self.write_file()
        
    def write_file(self):
        """
        Writes the GPX data to a file.
        """
        # If there are waypoints to write, write them to a file
        if self.waypoint_index > 0:
            # Construct the file name
            file_name = self.riverName + ' ' + self.waypoint_type + ' ' + str(self.file_index) + '.gpx'
            # Open the file and write the GPX data
            with open(file_name, 'w') as fo:
                fo.write(self.gpx.to_xml())
            # Increment the file index and reset the waypoint index and GPX object
            self.file_index += 1
            self.waypoint_index = 0
            self.gpx.waypoints.clear()

# Get the GPX file name from the command line arguments
if len(sys.argv) < 2:
    print("Usage: python parseRiverMaps.py <filename.gpx>")
    sys.exit(1)

gpx_file_name = sys.argv[1]

# Open the GPX file
with open(gpx_file_name) as gpx_file:
    # Create a GarminGpxFileWriter object for each type of waypoint
    waypoint_files = {
        'R-': GarminGpxFileWriter(gpx_file_name, 'Rapids'),
        'C-': GarminGpxFileWriter(gpx_file_name, 'Campgrounds'),
        'P-': GarminGpxFileWriter(gpx_file_name, 'POI'),
        'M-': GarminGpxFileWriter(gpx_file_name, 'Miles Markers')
    }

    # Parse the GPX file
    gpx = gpxpy.parse(gpx_file)

    # Loop over each waypoint in the GPX file
    for waypoint in gpx.waypoints:
        # Extract the waypoint type from the name
        key = waypoint.name[:2]

        # Check if the prefix is valid before processing to prevent KeyErrors
        if key in waypoint_files:
            # 1. Slice off the two-character prefix
            base_name = waypoint.name[2:].strip()
            suffix = ""

            # 2. Extract rapid class if it's a rapid
            if key == 'R-' and waypoint.description is not None:
                rapid_classification = re.search(r"(\(\w*)([0-9]+)(\w*\))", waypoint.description)
                if rapid_classification is not None:
                    # Drop the leading space to save another character
                    suffix = rapid_classification.group(2)
            
            # 3. Drop spaces and capitalize words for readability (PascalCase)
            base_name = base_name.title().replace(" ", "")
            
            # 4. Enforce the 15-character limit using vowel stripping
            max_base_len = 15 - len(suffix)
            
            if len(base_name) > max_base_len:
                # Strip vowels, but keep the first letter intact for readability
                first_char = base_name[0]
                rest_no_vowels = re.sub(r'[aeiouAEIOU]', '', base_name[1:])
                base_name = first_char + rest_no_vowels
                
                # If it is STILL too long after dropping vowels, apply a hard truncate
                base_name = base_name[:max_base_len]
            
            # Reconstruct the final, Garmin-safe name
            original_name = waypoint.name
            waypoint.name = base_name + suffix
            
            print(f'Processed: {original_name} -> {waypoint.name} ({waypoint.latitude},{waypoint.longitude})')

            # Add the waypoint to the appropriate file
            waypoint_files[key].add_waypoint(waypoint)
        else:
            print(f"Skipping unknown waypoint format: {waypoint.name}")

# Write the remaining waypoints to files
waypoint_files['R-'].write_file() 
waypoint_files['C-'].write_file() 
waypoint_files['P-'].write_file() 
waypoint_files['M-'].write_file()
