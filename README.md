# Rocket League Minimap Generator

**Version:** v1.0.0

## Installation

* Ensure [FFMPEG](http://ffmpeg.org/download.html) is installed and on the `PATH`

* `pip install -r requirements.txt --upgrade`
(A virtualenv type setup may be of value.)
**OR** download a precompiled version.

* Download rattletrap 
[https://github.com/tfausak/rattletrap/releases]()

## Usage Instructions

1. [Run rattletrap](https://github.com/tfausak/rattletrap#replays) on your 
replay file.
2. Run either `start.bat` or `start.sh` 
    * If you are running a precompiled version, run that 
    executable name instead.  Make sure that `field-template.svg` 
    and the `.json` file of the replay are next to the precompiled executable.

## Known Issues

* Players that disconnect, reconnect, or are replaced are not reflected 
accordingly in the generated minimap.  These players will remain on the field.
A later release will correct this issue.
* This program assumes that the ball has traveled the farthest possible in 
both the `X`, `Y`, and `Z` directions.  While the `Z` distance is not 
important yet, if the ball does not ever hit the boundaries of the map, then 
the size of the field is not accurately displayed.  In a later version, both 
the players and the ball will be used in the calculation of the field 
boundaries.
