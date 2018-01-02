def render_video(out_prefix, render_type,
                 out_frame_rate=30, overlay=None, extra_cmd=None):
    import os
    import subprocess
    from pathlib import Path

    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.main import frame_num_format

    Path(os.path.join(out_prefix, render_type + '-frames.txt')).touch()

    with open(os.path.join(out_prefix, render_type + '-frames.txt'),
              'w') as f:
        out_str = ''
        for i, frame in enumerate(
                get_frames()):
            out_str += 'file \'' + os.path.join(out_prefix, render_type,
                                                frame_num_format.format(
                                                        i) + '.png') + '\'\n'
            out_str += 'duration ' + \
                       str(frame['time']['real_replay_delta']) + '\n'
        # Ensure display of final frame
        out_str += 'file \'' + os.path.join(out_prefix, render_type,
                                            frame_num_format.format(
                                                    len(get_frames())) +
                                            '.png') + \
                   '\'\n'
        f.write(out_str)

    cmd = ['ffmpeg',
           '-i',
           os.path.join('assets', overlay + '.png'),
           '-safe', '0',
           '-f', 'concat',
           '-i',
           os.path.join(out_prefix,
                        render_type + '-frames.txt'),
           '-filter_complex', '[0:v] overlay',
           '-r', str(out_frame_rate)]

    cmd += extra_cmd

    cmd += ['-crf', '18',
            os.path.join(out_prefix,
                         render_type + '-' + overlay +
                         '.mp4'),
            '-y']

    print('Command', cmd)

    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT)

    p.communicate()
