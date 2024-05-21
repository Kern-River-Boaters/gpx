import gpxpy
import gpxpy.gpx
import sys
from pathlib import Path
import re

class GarminGpxFileWriter:
    def __init__(self, gpx_file_name, wayPointType):
        self.wayPointType = wayPointType
        self.fileNum = 1
        self.wayPointIndex = 0
        self.gpx = gpxpy.gpx.GPX()
        self.riverName = Path(gpx_file_name).stem
        
    def addWayPoint(self,wayPoint):
        if ( self.wayPointIndex == 99):
            self.writeFile()
        self.wayPointIndex = self.wayPointIndex + 1
        wayPoint.name = wayPoint.name[2:]
        wayPoint.extensions.clear()
        self.gpx.waypoints.append(wayPoint)
        
    def writeFile(self):
        if (self.wayPointIndex > 0):
            fileName = self.riverName + ' ' + self.wayPointType + ' ' + str(self.fileNum) + '.gpx'
            fo = open(fileName , 'w')
            fo.write(self.gpx.to_xml())
            fo.close()
            self.fileNum = self.fileNum + 1
            self.wayPointIndex = 0
            self.gpx.waypoints.clear()
        

# Parse river file
gpx_file_name = sys.argv[1]
gpx_file = open(gpx_file_name)

waypointFiles = {
    'R-': GarminGpxFileWriter(gpx_file_name, 'Rapids'), 
    'C-': GarminGpxFileWriter(gpx_file_name, 'Campgrounds'), 
    'P-': GarminGpxFileWriter(gpx_file_name, 'POI'), 
    'M-': GarminGpxFileWriter(gpx_file_name, 'Miles Markers')} 

gpx = gpxpy.parse(gpx_file)

for waypoint in gpx.waypoints:
    print(f'waypoint {waypoint.name} -> ({waypoint.latitude},{waypoint.longitude})')
    key = waypoint.name[:2]
    if key == 'R-' and waypoint.description is not None:
        rapidClass = re.search("(\(\w*)([0-9]+)(\w*\))",waypoint.description)
        if rapidClass is not None:
            waypoint.name = waypoint.name + ' ' + rapidClass.group(2)
    waypointFiles[key].addWayPoint(waypoint)

# Write the remaining waypoints before exiting
waypointFiles['R-'].writeFile() 
waypointFiles['C-'].writeFile() 
waypointFiles['P-'].writeFile() 
waypointFiles['M-'].writeFile() 