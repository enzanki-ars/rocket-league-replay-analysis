def render_video(render_type,
                 out_frame_rate=30, overlay=None, extra_cmd=None):
    import os
    import subprocess

    from rocketleaguereplayanalysis.render.do_render import get_video_prefix
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.sync import get_sync_time_type

    video_prefix = get_video_prefix()

    cmd = ['ffmpeg',
           '-loop', '1',
           '-i', os.path.join('assets', overlay + '.png'),
           '-t', str(get_frames()[-1]['time'][get_sync_time_type()])]

    cmd += extra_cmd

    cmd += ['-r', str(out_frame_rate),
            '-crf', '18',
            render_type + '.mp4', '-y']

    print('FFmpeg Command:', cmd)

    p = subprocess.Popen(cmd, cwd=video_prefix, stderr=subprocess.STDOUT)

    p.communicate()
