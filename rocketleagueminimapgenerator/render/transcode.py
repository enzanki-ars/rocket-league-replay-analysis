def render_video(out_prefix, type, out_frame_rate=30):
    import os
    import subprocess
    from pathlib import Path

    from rocketleagueminimapgenerator.parser.frames import get_frames
    from rocketleagueminimapgenerator.main import frame_num_format
    from rocketleagueminimapgenerator.data.data import get_data_start, \
        get_data_end

    Path(os.path.join(out_prefix, type + '-frames.txt')).touch()

    with open(os.path.join(out_prefix, type + '-frames.txt'),
              'w') as f:
        out_str = ''
        for i, frame in enumerate(
                get_frames()[get_data_start():get_data_end()]):
            out_str += 'file \'' + os.path.join(out_prefix, type,
                                                frame_num_format.format(
                                                        i) + '.png') + '\'\n'
            out_str += 'duration ' + str(frame['delta']) + '\n'
        # Ensure display of final frame
        out_str += 'file \'' + os.path.join(out_prefix, type,
                                            frame_num_format.format(
                                                    get_data_end()) +
                                            '.png') + \
                   '\'\n'
        f.write(out_str)

    p = subprocess.Popen(['ffmpeg',
                          '-safe', '0',
                          '-f', 'concat',
                          '-i', os.path.join(out_prefix, type + '-frames.txt'),
                          '-r', str(out_frame_rate),
                          '-vf', 'format=yuv420p',
                          '-crf', '18',
                          os.path.join(out_prefix, type + '.mp4'),
                          '-y'],
                         stderr=subprocess.STDOUT)

    p.communicate()