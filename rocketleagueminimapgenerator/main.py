import os

from rocketleagueminimapgenerator.actor_data import parse_actor_data
from rocketleagueminimapgenerator.data import load_data
from rocketleagueminimapgenerator.frames import load_frames
from rocketleagueminimapgenerator.object_numbers import parse_ball_obj_nums, \
    parse_car_obj_nums, parse_player_info
from rocketleagueminimapgenerator.render import render_field, render_video

with open('field-template.svg', 'r') as svg_file:
    field_template = svg_file.read()

car_template = '<circle class="team{team_id} stroke-black" ' \
               'cx="{car_pos_y}" cy="{car_pos_x}" r="{car_size}"/>'
frame_num_format = '{0:04d}'


def main():
    print('Please enter the name of the game json without the file extension.')
    out_prefix = input('> ')

    load_data(out_prefix)
    parse_actor_data()

    parse_ball_obj_nums()
    parse_car_obj_nums()
    parse_player_info()

    load_frames()

    video_prefix = os.path.join('renders', out_prefix)

    render_field(video_prefix)

    render_video(video_prefix)


if __name__ == "__main__":
    main()
