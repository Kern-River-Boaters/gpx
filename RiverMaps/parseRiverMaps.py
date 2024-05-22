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
        Add a waypoint to the GPX file.

        Args:
            waypoint (gpxpy.gpx.GPXWaypoint): The waypoint to add.
        """
        # If we've reached the maximum number of waypoints per file, write the current file
        if self.waypoint_index == 99:
            self.write_file()
        # Increment the waypoint index
        self.waypoint_index += 1
        # Modify the waypoint name and clear its extensions
        waypoint.name = waypoint.name[2:]
        waypoint.extensions.clear()
        # Add the waypoint to the GPX object
        self.gpx.waypoints.append(waypoint)
        
    def write_file(self):
        """
        Writes the GPX data to a file.

        If the waypoint index is greater than 0, it creates a file name based on the river name, waypoint type, and file index.
        Then, it opens the file in write mode and writes the GPX data to it using the `to_xml()` method of the `gpx` object.
        After writing the data, it increments the file index, resets the waypoint index to 0, and clears the waypoints list in the `gpx` object.
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
        # Print the waypoint's name and coordinates
        print(f'waypoint {waypoint.name} -> ({waypoint.latitude},{waypoint.longitude})')

        # Extract the waypoint type from the name
        key = waypoint.name[:2]

        # If the waypoint is a rapid and has a description, add the rapid class to the name
        if key == 'R-' and waypoint.description is not None:
            rapid_classification = re.search(r"(\(\w*)([0-9]+)(\w*\))", waypoint.description)
            if rapid_classification is not None:
                waypoint.name += ' ' + rapid_classification.group(2)

        # Add the waypoint to the appropriate file
        waypoint_files[key].add_waypoint(waypoint)

# Write the remaining waypoints to files
waypoint_files['R-'].write_file() 
waypoint_files['C-'].write_file() 
waypoint_files['P-'].write_file() 
waypoint_files['M-'].write_file()