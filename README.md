# Kern River Boater GPX collections
Garmin GPX Files Optimized for the Garmin Instinct.  The Garmin Instinct has 15 character name limits.

## Instuctions
Currently, the best way to import this is using a PC web brower and opening https://explore.garmin.com/Map

* On your Garmin watch, add the map view for the kayak activity
* Import each file as a new collection https://explore.garmin.com/Map.  Note, you can import the waypoint file as Tracks or Routes.
* Select all of the waypoints in each collection to set an icon.  I recommend these icons as they render nicely on the Instinct: ![Garmin Icons](garmin-icons.png)

# Other resources
Many river (Salt, Grand Canyon, Green, etc.) GPX files are available from https://rivermaps.net/pages/gps-waypoints. 
I recommend breaking them up into different categories, campsites, milestones, POI, and rapids.  Additionally, the files should be a max of 99 waypoints as that seems to be a Collection size limitation in some Garmin devices.  To assist with this preprocessing, I have included a parseRiverMaps.py script to automate breaking apart the GPX into multiple GPX files.
