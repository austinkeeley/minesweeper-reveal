# minesweeper-reveal.py
# A Python script that shows the locations of mines in winmine.exe by examining
# the processes's memory. Requires winappdbg.

from __future__ import print_function
import struct

from winappdbg import Process

# Start of the border of the mine field
MINEFIELD_START = 0x01005340
MINEFIELD_BORDER_BYTE =  '\x10'
MINE_MASK = '\x80'

def byte_to_int(bytestring):
    """Helper function to convert a bytestring to an integer"""
    return struct.unpack('B', bytestring)[0]

def get_minefield_size(process):
    """Gets the size of the minefield in a winmine.exe process, not including
    the border
    Args:
        process (winappdbg.Process): The process to get the size from
    Returns:
        A tuple in the form of (width, height)

    """
    width = 0
    height = 0

    # Get the width
    border = process.read(MINEFIELD_START, 1)
    while border == MINEFIELD_BORDER_BYTE and width < 32:
        width = width + 1
        border = process.read(MINEFIELD_START + width, 1)

    # Get the height
    border = process.read(MINEFIELD_START, 1)
    while border == MINEFIELD_BORDER_BYTE:
        height = height + 1
        border = process.read(MINEFIELD_START + (height * 32), 1)

    return (width - 2, height - 2)  # subtract 2 for the border


def find_mines(process, width, height):
    """Finds the mines in the process.
    Args:
        process (winappdbg.Process): The winmine.exe process to search through
        width (int): The game width
        height (int): The game height
    Returns:
        A list of strings, where each string contains a row of the game and the
        mine locations
    """
    result = []
    for h in xrange(height + 2):
        row = ''
        for w in xrange(width + 2):
            cell = process.read(MINEFIELD_START + (h * 32) + w, 1)
            if cell == '\x10':
                row += '#'
            elif byte_to_int(cell) & byte_to_int(MINE_MASK):
                row += '*'
            else:
                row += '.'
        result.append(row)
    return result

def main(pid):
    """Main function
    Args:
        pid (int): The pid to connect to

    """
    process = Process(pid)

    width, height = get_minefield_size(process)
    print('Width is %d' % width)
    print('Height is %d' % height)
    print()
    print('\n'.join(find_mines(process, width, height)))


if __name__ == '__main__':
    print('Minesweeper Reveal')
    pid = int(raw_input('Enter the PID of winmine.exe: '))
    main(pid)





