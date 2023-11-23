#!/usr/bin/env python3

from math import ceil
from string import Template

WALL_COLUMN_COUNTS = [17, 18]
INNER_COLUMN_COUNT = 13

TILE_WIDTH = 28
TILE_HEIGHT = 37
TILE_ROUNDING_RADIUS = 5
TILE_FILL = "green"
TILE_BORDER = "black"
TILE_BORDER_WIDTH = 2

ILLUSTRATION_TEMPLATE = Template(f'''\
<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="$view_left $view_top $view_width $view_height" xmlns="http://www.w3.org/2000/svg">
<defs>
  <rect id="tile"
    width="$tile_width" height="$tile_height"
    rx="$rounding_radius" ry="$rounding_radius"
    fill="$tile_fill" stroke="$tile_border" stroke-width="$tile_border_width"
    />
</defs>
$walls_content
</svg>
''')


def build_svg(column_count, show_starts):
    view_width = 1.1 * (2 * column_count - INNER_COLUMN_COUNT) * TILE_WIDTH
    inner_side_length = INNER_COLUMN_COUNT * TILE_WIDTH

    east_first_tile_left = inner_side_length/2 - TILE_WIDTH
    east_first_tile_top = inner_side_length/2

    single_wall = '\n'.join(
        f'<use href="#tile" x="{east_first_tile_left - column_index * TILE_WIDTH}" y="{east_first_tile_top}" />'
        for column_index in range(column_count)
    )
    four_walls = '\n'.join(
        f'<g transform="rotate({wall_index * 90})">\n{single_wall}\n</g>'
        for wall_index in range(0, 4)
    )

    walls_content = four_walls  # TODO

    svg_content = ILLUSTRATION_TEMPLATE.substitute(
        view_left=-view_width/2,
        view_top=-view_width/2,
        view_width=view_width,
        view_height=view_width,
        tile_width=TILE_WIDTH,
        tile_height=TILE_HEIGHT,
        rounding_radius=TILE_ROUNDING_RADIUS,
        tile_fill=TILE_FILL,
        tile_border=TILE_BORDER,
        tile_border_width=TILE_BORDER_WIDTH,
        walls_content=walls_content,
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
