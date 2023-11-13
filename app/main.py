from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from microbmp import MicroBMP

if TYPE_CHECKING:
    from typing import Optional, Tuple

black_pixels = []
steps = 0
steps_limit = 100000
direction = 'top'
current_position = (512, 512)
field_size = (1024, 1024)


def main() -> None:
    """Run application."""
    global steps
    global steps_limit
    global current_position
    global field_size
    global black_pixels
    while True:
        if steps >= steps_limit:
            sys.stdout.write(f'Were made {steps} steps')
            break
        if current_position[0] < 0 or current_position[0] >= field_size[0]:
            sys.stdout.write(f'The ant has left X axis')
            break
        if current_position[1] < 0 or current_position[1] >= field_size[1]:
            sys.stdout.write(f'The ant has left Y axis')
            break
        move_ant()
    create_image_file()
    sys.stdout.write(f'Black points: {len(black_pixels)}')


def move_ant() -> None:
    """Move ant."""
    global steps
    global current_position
    index_of_black = get_index_of_black(current_position)
    if index_of_black is None:
        # White pixel
        turn_right()
    else:
        # Black pixel
        turn_left()
    invert_color(index_of_black)
    make_step()
    steps += 1


def make_step() -> None:
    """Make step."""
    global direction
    global current_position
    match direction:
        case 'top':
            current_position = (current_position[0], current_position[1] + 1)
        case 'right':
            current_position = (current_position[0] + 1, current_position[1])
        case 'bottom':
            current_position = (current_position[0], current_position[1] - 1)
        case 'left':
            current_position = (current_position[0] - 1, current_position[1])


def invert_color(index_of_black: Optional[int]) -> None:
    """Invert color."""
    global black_pixels
    global current_position
    if index_of_black is None:
        black_pixels.append(current_position)
    else:
        black_pixels.remove(current_position)


def turn_right() -> None:
    """Turn ant right."""
    global direction
    match direction:
        case 'top':
            direction = 'right'
        case 'right':
            direction = 'bottom'
        case 'bottom':
            direction = 'left'
        case 'left':
            direction = 'top'


def turn_left() -> None:
    """Turn ant left."""
    global direction
    match direction:
        case 'top':
            direction = 'left'
        case 'left':
            direction = 'bottom'
        case 'bottom':
            direction = 'right'
        case 'right':
            direction = 'top'


def create_image_file() -> None:
    """Create image file."""
    global field_size
    global black_pixels
    bmp_img = MicroBMP(field_size[0], field_size[1], 1)
    white_array = b'\xFF' * len(bmp_img.parray)
    bmp_img.parray = bytearray(white_array)
    for coord in black_pixels:
        bmp_img[coord[1], coord[0]] = 0
    bmp_img.save('langton_ant.bmp')


def get_index_of_black(position: Tuple[int, int]) -> Optional[int]:
    """Try to get index of black pixel."""
    try:
        return black_pixels.index(position)
    except ValueError:
        return None


if __name__ == '__main__':
    main()
