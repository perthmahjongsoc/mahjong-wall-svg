#!/usr/bin/env python3

from math import ceil
from string import Template

WALL_COLUMN_COUNTS = [17, 18]

TILE_WIDTH = 28
TILE_HEIGHT = 37
VIEW_HALF_WIDTH = ceil(1.3 * max(WALL_COLUMN_COUNTS) / 2 * TILE_WIDTH)

ILLUSTRATION_TEMPLATE = Template(f'''\
<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="$view_left $view_top $view_width $view_height">
</svg>
''')


def build_svg(column_count, show_starts):
    svg_content = ILLUSTRATION_TEMPLATE.substitute(
        view_left=-VIEW_HALF_WIDTH,
        view_top=-VIEW_HALF_WIDTH,
        view_width=2 * VIEW_HALF_WIDTH,
        view_height=2 * VIEW_HALF_WIDTH,
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
