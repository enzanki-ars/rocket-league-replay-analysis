# Rocket League Replay Analysis

**Version:** v1.4.0-alpha1

## Licences

- This project is licensed under the GNU Affero General Public License v3.0
  - See `LICENSE.md` for more info.
- Open Sans by Google Fonts licensed under Apache License Version 2.0
  - See `assets/Google-Fonts-OpenSans-LICENSE.txt` for more info.

## Installation

* Ensure [FFMPEG](http://ffmpeg.org/download.html) is installed and on the `PATH`

* Download a precompiled version or download the sourcecode.

## Usage Instructions

1. Run RocketLeagueReplayParser on your replay file.
    * Instructions coming soon for using RocketLeagueReplayParser.
2. Run `python -m rocketleaguereplayanalysis.main [args]` replacing 
`[args]` with the program arguments you wish to use.  Leave empty to see help.
    * If you are running a precompiled version, run that 
    executable name instead, for example `rocketleaguereplayanalysis.exe`

```
usage: rocketleaguereplayanalysis 
                                  [-h]
                                  [--render {player-data-drive,
                                             player-data-scoreboard,
                                             possession,
                                             pressure,
                                             scoreboard} 
                                       [{player-data-drive,
                                         player-data-scoreboard,
                                         possession,
                                         pressure,
                                         scoreboard} ...]]
                                  [--data_explorer] 
                                  [--export_parsed_data]
                                  [--show_field_size] 
                                  [--version]
                                  game_json

positional arguments:
  game_json             The name of the game json.

optional arguments:
  -h, --help            show this help message and exit
  --render {player-data-drive,
            player-data-scoreboard,
            possession,
            pressure,
            scoreboard} 
            [{player-data-drive,
              player-data-scoreboard,
              possession,
              pressure,
              scoreboard} ...]
                        Select which renders are created. 
                        Multiple renders can be separated by a space.
  --data_explorer       Explore the given data.
  --export_parsed_data  Export the parsed data.
  --show_field_size     Show the calculated field size.
  --version             Print version and exit (v1.4.0-alpha1)
```

## Known Issues

* This program assumes that the ball has traveled the farthest from center 
in both the `X`, `Y`, and `Z` directions, though the `Z` distance is not 
important yet.  If the ball does not ever hit the side boundary of the map, 
then the size of the field is not accurately displayed.  In a later version, 
both the players and the ball will be used in the calculation of the field 
boundaries.
