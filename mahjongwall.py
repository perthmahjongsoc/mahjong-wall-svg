#!/usr/bin/env python3

from math import pi, cos, sin
from string import Template

WALL_TILT_DEGREES = 22.5
WALL_COLUMN_COUNTS = [17, 18]
INNER_COLUMN_COUNT = 13

TILE_WIDTH = 28
TILE_HEIGHT = 37
TILE_ROUNDING_RADIUS = 5
TILE_FILL = 'green'
TILE_BORDER = 'black'
TILE_BORDER_WIDTH = 2

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
  #tile {
    fill: $tile_fill;
    stroke: $tile_border;
    stroke-width: $tile_border_width;
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
  <rect id="tile" width="$tile_width" height="$tile_height" rx="$rounding_radius" ry="$rounding_radius" />
</defs>
$table_content_tilted
</svg>
''')


def build_single_wall(wall_index, column_count, inner_side_length):
    initial_left = inner_side_length/2 - TILE_WIDTH
    initial_top = inner_side_length/2
    overhang_column_count = column_count - INNER_COLUMN_COUNT

    return '\n'.join(
        f'<use href="#tile" x="{initial_left - column_index * TILE_WIDTH}" y="{initial_top}" />'
        f'<g transform="'
        f'rotate({WALL_TILT_DEGREES}) '
        f'translate({initial_left} {initial_top + overhang_column_count * TILE_WIDTH}) '
        f'rotate({-wall_index * 90})'
        f'"><text class="wind">{WIND_TEXT_FROM_INDEX[wall_index]}</text></g>'
        for column_index in range(column_count)
    )


def build_svg(column_count, show_starts):
    wall_tilt = WALL_TILT_DEGREES * pi / 180
    view_width = (2 * column_count - INNER_COLUMN_COUNT) * TILE_WIDTH * (cos(wall_tilt) + sin(wall_tilt))
    inner_side_length = INNER_COLUMN_COUNT * TILE_WIDTH

    four_walls = '\n'.join(
        f'<g transform="rotate({wall_index * 90})">\n'
        f'{build_single_wall(wall_index, column_count, inner_side_length)}\n'
        f'</g>'
        for wall_index in range(0, 4)
    )

    table_content = four_walls  # TODO

    table_content_tilted = f'<g transform="rotate(-{WALL_TILT_DEGREES})">\n{table_content}\n</g>'

    svg_content = ILLUSTRATION_TEMPLATE.substitute(
        view_left=-view_width/2,
        view_top=-view_width/2,
        view_width=view_width,
        view_height=view_width,
        wind_font_size=WIND_FONT_SIZE,
        tile_width=TILE_WIDTH,
        tile_height=TILE_HEIGHT,
        rounding_radius=TILE_ROUNDING_RADIUS,
        tile_fill=TILE_FILL,
        tile_border=TILE_BORDER,
        tile_border_width=TILE_BORDER_WIDTH,
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
