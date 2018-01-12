# Rocket League Replay Analysis

**Version:** v1.4.0-alpha1

## Licences

- This project is licensed under the GNU Affero General Public License v3.0
  - See `LICENSE.md` for more info.
- Open Sans by Google Fonts licensed under Apache License Version 2.0
  - See `assets/Google-Fonts-OpenSans-LICENSE.txt` for more info.

## Installation

* A replay from Rocket League
  * Windows: `Documents\My Games\Rocket League\TAGame\Demos`
  * macOS: `Library/Application Support/Rocket League/TAGame/Demos`
  * Linux: `$HOME/.local/share/Rocket League/TAGame/Demos`
* Ensure [FFMPEG](http://ffmpeg.org/download.html) is installed and on the `PATH`
  * Windows: Make sure to add it to the path.
    1. Copy the path of the folder you installed FFmpeg to in explorer while in the "bin" pat
    2. Open the start menu (or Cortana…) and search for "Environment Variables"
    3. Select "Edit the system environment variables"
    4. Select "Environment Variables…" at the bottom of the window.
    5. In the "User Variables" section, click on "Path" and select "Edit"
    6. Click "New" and paste the FFmpeg path. Make sure it ends with bin, otherwise reread line 1.
* Download [RocketLeagueReplayParser](https://github.com/jjbott/RocketLeagueReplayParser/releases)
  * Linux/Mac Only: I am not certain this tool works on this platform. The
  README claims that it does not, but I doubt this... I will update this
  with more information soon.  If it does work, you will need to install
  [Mono](http://www.mono-project.com/).
* Download a precompiled version or download the sourcecode.
  * Currently, I only compile builds for Windows. Linux/Mac users can use
  the `Source code (zip)` option.

## Usage Instructions

1. Run RocketLeagueReplayParser on your replay file.
    * Note for Mac/Linux users: Add `mono` to the beginning of all of the 
    commands for RocketLeagueReplayParser.
    * Run `RocketLeagueReplayParser.exe example.replay --fileoutput`
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
                                             scoreboard,
                                             total-boost} 
                                       [{player-data-drive,
                                         player-data-scoreboard,
                                         possession,
                                         pressure,
                                         scoreboard,
                                         total-boost} ...]]
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
            scoreboard,
            total-boost} 
            [{player-data-drive,
              player-data-scoreboard,
              possession,
              pressure,
              scoreboard,
              total-boost} ...]
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
