# Rocket League Replay Analysis

**Version:** v1.3.1-dev

## Licences

- This project is licensed under the GNU Affero General Public License v3.0
  - See `LICENSE.md` for more info.
- Open Sans by Google Fonts licensed under Apache License Version 2.0
  - See `assets/Google-Fonts-OpenSans-LICENSE.txt` for more info.

## Installation

* Ensure [FFMPEG](http://ffmpeg.org/download.html) is installed and on the `PATH`

* `pip install -r requirements.txt --upgrade`
(A virtualenv type setup may be of value.)
**OR** download a precompiled version.

* **_Highly Suggested:_** A [RAM disk](https://sourceforge.net/projects/imdisk-toolkit/) 
is suggested to run the program much faster.  This program can take up about 
.1 GB per minimap render, with player data renders taking up about .2 GB per 
render.  A RAM Disk does not necessarily increase the program's speed, but it 
will help reduce the stress on the hard drive.  Copy the program to the RAM 
disk and run it from there.

## Usage Instructions

1. Run RocketLeagueReplayParser on your replay file.
    * Instructions coming soon for using RocketLeagueReplayParser.
2. Run `python -m rocketleaguereplayanalysis.main [args]` replacing 
`[args]` with the program arguments you wish to use.  Leave empty to see help.
    * If you are running a precompiled version, run that 
    executable name instead.

```
usage: rocketleaguereplayanalysis [-h]
                                  [--process_type {video_minimap,
                                                   video_pressure,
                                                   video_possession,
                                                   video_player_data_drive,
                                                   video_player_data_scoreboard,
                                                   video_all,
                                                   data_explorer}]
                                  [--export_parsed_data]
                                  [--version]
                                  game_json

positional arguments:
  game_json             The name of the game json.

optional arguments:
  -h, --help            show this help message and exit
  --process_type        {video_minimap,video_pressure,video_possession,
                         video_player_data_drive,video_player_data_scoreboard,
                         video_player_data_scoreboard_with_drive,
                         video_all,data_explorer}
  --export_parsed_data  Export the parsed data.
  --version             Print version and exit
```

## Known Issues

* This program assumes that the ball has traveled the farthest from center 
in both the `X`, `Y`, and `Z` directions, though the `Z` distance is not 
important yet.  If the ball does not ever hit the side boundary of the map, 
then the size of the field is not accurately displayed.  In a later version, 
both the players and the ball will be used in the calculation of the field 
boundaries.
