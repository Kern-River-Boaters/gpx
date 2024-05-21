# Kern River Boater GPX collections
Garmin GPX Files Optimized for the Garmin Instinct.  The Garmin Instinct has 15 character name limits.

## Instuctions
Currently, the best way to import this is using a PC web brower and opening https://explore.garmin.com/Map

* On your Garmin watch, add the map view for the kayak activity
* Import each file as a new collection https://explore.garmin.com/Map.  Note, you can import the waypoint file as Tracks or Routes.
* Select all of the waypoints in each collection to set an icon.  I recommend these icons as they render nicely on the Instinct: ![Garmin Icons](garmin-icons.png)

# Other resources
Many river (Salt, Grand Canyon, Green, etc.) GPX files are available from https://rivermaps.net/pages/gps-waypoints. 
I recommend breaking them up into different categories, campsites, milestones, POI, and rapids.  Additionally, I recommend breaking apart the files into 99 waypoints or less as there is a warning in the Garmin Explorer App incidicating the collection is too large.  The parseRiverMaps.py script in this repo automates this process.  Additionally, it appends the rapid class to the waypoint name.


