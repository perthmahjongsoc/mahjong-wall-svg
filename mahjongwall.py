#!/usr/bin/env python3

from math import pi, cos, sin
from string import Template

WALL_TILT_DEGREES = 23.4
WALL_COLUMN_COUNTS = [17, 18]
INNER_COLUMN_COUNT = 13

DICE_ROLL_MIN = 3
DICE_ROLL_MAX = 18

TILE_WIDTH = 28
TILE_HEIGHT = 37
TILE_ROUNDING_RADIUS = 5
TILE_FILL_COLOUR = 'green'
TILE_BORDER_COLOUR = 'black'
TILE_BORDER_WIDTH = 2

START_COLOUR = 'crimson'
START_LINE_WIDTH = 5
START_FONT_SIZE = '36px'

WIND_TEXT_FROM_INDEX = {
    0: '東 E',
    1: '南 S',
    2: '西 W',
    3: '北 N',
}
WIND_FONT_SIZE = '72px'

ILLUSTRATION_TEMPLATE = Template('''\
<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="$view_left $view_top $view_width $view_height" xmlns="http://www.w3.org/2000/svg">
<style>
  #arrowhead {
    fill: $start_colour;
  }
  #start {
    fill: none;
    stroke: $start_colour;
    stroke-width: $start_line_width;
  }
  #tile {
    fill: $tile_fill_colour;
    stroke: $tile_border_colour;
    stroke-width: $tile_border_width;
  }
  .start {
    font: $start_font_size sans-serif;
    fill: $start_colour;
  }
  .wind {
    font: $wind_font_size sans-serif;
  }
  text {
    dominant-baseline: middle;
    text-anchor: middle;
  }
</style>
<defs>
  <marker id="arrowhead" viewBox="0 -15 50 30" refX="25" refY="0"
    markerUnits="userSpaceOnUse" markerWidth="50" markerHeight="15" orient="auto-start-reverse">
    <path d="M 0 -15 L 0 15 L 50 0 z"/>
  </marker>
  <path id="start" marker-end="url(#arrowhead)" d="M 0 0 v $start_height h -$start_width" />
  <rect id="tile" width="$tile_width" height="$tile_height" rx="$rounding_radius" ry="$rounding_radius" />
</defs>
$table_content_tilted
</svg>
''')


def shrink_if(predicate):
    if predicate:
        return 0.9
    else:
        return 1


def build_single_wall(wall_index, column_count, inner_side_length):
    initial_left = inner_side_length/2 - TILE_WIDTH
    initial_top = inner_side_length/2

    east_wall = '\n'.join(
        f'<use href="#tile" x="{initial_left - column_index * TILE_WIDTH}" y="{initial_top}" />'
        f'<g transform="'
        f'translate({initial_left - 4 * TILE_HEIGHT} {initial_top + shrink_if(wall_index == 2) * 4.8 * TILE_HEIGHT}) '
        f'rotate({WALL_TILT_DEGREES + wall_index * 90})'
        f'"><text class="wind">{WIND_TEXT_FROM_INDEX[wall_index]}</text></g>'
        for column_index in range(column_count)
    )

    return f'<g transform="rotate({-wall_index * 90})">\n{east_wall}\n</g>'


def build_single_start(dice_roll, column_count, inner_side_length):
    wall_index = (dice_roll - 1) % 4 - dice_roll // column_count
    slit_index = dice_roll % column_count

    tail_x = inner_side_length/2 - slit_index * TILE_WIDTH
    tail_y = inner_side_length/2 + TILE_HEIGHT

    east_start = (
        f'<use href="#start" x="{tail_x}" y="{tail_y}" />'
        f'<g transform="'
        f'translate('
        f'{tail_x - (0.2 if dice_roll < column_count else 0.8) * TILE_HEIGHT} '
        f'{tail_y + shrink_if(wall_index == 2 or dice_roll < 10) * 1.4 * TILE_HEIGHT}'
        f') '
        f'rotate({WALL_TILT_DEGREES + wall_index * 90}) '
        f'"><text class="start">{dice_roll}</text></g>'
    )

    return f'<g transform="rotate({-wall_index * 90})">\n{east_start}\n</g>'


def build_svg(column_count, show_starts):
    wall_tilt = WALL_TILT_DEGREES * pi / 180
    view_width = (2 * max(WALL_COLUMN_COUNTS) - INNER_COLUMN_COUNT) * TILE_WIDTH * (cos(wall_tilt) + sin(wall_tilt))
    inner_side_length = INNER_COLUMN_COUNT * TILE_WIDTH

    start_width = 2.5 * TILE_WIDTH
    start_height = 1/2 * TILE_HEIGHT

    four_walls = '\n'.join(
        build_single_wall(wall_index, column_count, inner_side_length)
        for wall_index in range(0, 4)
    )
    starts = '\n'.join(
        build_single_start(dice_roll, column_count, inner_side_length)
        for dice_roll in range(DICE_ROLL_MIN, DICE_ROLL_MAX + 1)
    )

    table_content = four_walls + (f'\n{starts}' if show_starts else '')
    table_content_tilted = f'<g transform="rotate(-{WALL_TILT_DEGREES})">\n{table_content}\n</g>'

    svg_content = ILLUSTRATION_TEMPLATE.substitute(
        view_left=-view_width/2,
        view_top=-view_width/2,
        view_width=view_width,
        view_height=view_width,
        tile_width=TILE_WIDTH,
        tile_height=TILE_HEIGHT,
        start_width=start_width,
        start_height=start_height,
        rounding_radius=TILE_ROUNDING_RADIUS,
        tile_fill_colour=TILE_FILL_COLOUR,
        tile_border_colour=TILE_BORDER_COLOUR,
        tile_border_width=TILE_BORDER_WIDTH,
        start_colour=START_COLOUR,
        start_line_width=START_LINE_WIDTH,
        start_font_size=START_FONT_SIZE,
        wind_font_size=WIND_FONT_SIZE,
        table_content_tilted=table_content_tilted,
    )
    return svg_content


def main():
    for column_count in WALL_COLUMN_COUNTS:
        for show_starts in [True, False]:
            svg_file_name = f'mahjong-wall-{column_count}-columns{"-with-start" if show_starts else ""}.svg'
            svg_content = build_svg(column_count, show_starts)
            with open(svg_file_name, 'w') as svg_file:
                svg_file.write(svg_content)


if __name__ == '__main__':
    main()
