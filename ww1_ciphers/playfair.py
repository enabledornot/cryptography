import string
import textwrap
import sys
from tools import *
def playfair_grid(codeword):
    codeword = clean_text(codeword)
    grid = []
    for c in codeword:
        if c not in grid:
            grid.append(c)
    for c in string.ascii_lowercase:
        if c == 'j':
            continue
        if c not in grid:
            grid.append(c)
    return grid
def playfair_segment(message):
    return textwrap.wrap(message, width=2)
def playfair_grid_row_column(letter, grid):
    letter_index = grid.index(letter)
    return letter_index // 5, letter_index % 5
def playfair_grid_get(row, column, grid):
    row = row % 5
    column = column % 5
    return grid[row*5 + column]
def playfair_translate_e(segment, grid):
    # letter 0 row, letter 0 column
    l_0_r, l_0_c = playfair_grid_row_column(segment[0], grid)
    if len(segment) == 1 or segment[0] == segment[1]:
        l_1_r, l_1_c = playfair_grid_row_column("x", grid)
    else:
        l_1_r, l_1_c = playfair_grid_row_column(segment[1], grid)
    # t_0 = translated 0 letter
    if l_0_r == l_1_r:
        t_0 = playfair_grid_get(l_0_r, l_0_c + 1, grid)
        t_1 = playfair_grid_get(l_1_r, l_1_c + 1, grid)
    elif l_0_c == l_1_c:
        t_0 = playfair_grid_get(l_0_r + 1, l_0_c, grid)
        t_1 = playfair_grid_get(l_1_r + 1, l_1_c, grid)
    else:
        t_0 = playfair_grid_get(l_0_r, l_1_c, grid)
        t_1 = playfair_grid_get(l_1_r, l_0_c, grid)
    return t_0 + t_1
def playfair_translate_d(segment, grid):
    # letter 0 row, letter 0 column
    l_0_r, l_0_c = playfair_grid_row_column(segment[0], grid)
    l_1_r, l_1_c = playfair_grid_row_column(segment[1], grid)
    # t_0 = translated 0 letter
    if l_0_r == l_1_r:
        t_0 = playfair_grid_get(l_0_r, l_0_c - 1, grid)
        t_1 = playfair_grid_get(l_1_r, l_1_c - 1, grid)
    elif l_0_c == l_1_c:
        t_0 = playfair_grid_get(l_0_r - 1, l_0_c, grid)
        t_1 = playfair_grid_get(l_1_r - 1, l_1_c, grid)
    else:
        t_0 = playfair_grid_get(l_0_r, l_1_c, grid)
        t_1 = playfair_grid_get(l_1_r, l_0_c, grid)
    return t_0 + t_1
def playfair_e(codeword, d_message):
    grid = playfair_grid(codeword)
    e_message = ""
    for segment in playfair_segment(d_message):
        e_message += playfair_translate_e(segment, grid)
    return e_message
def playfair_d(codeword, e_message):
    grid = playfair_grid(codeword)
    d_message = ""
    for segment in playfair_segment(e_message):
        d_message += playfair_translate_d(segment, grid)
    return d_message

if __name__ == "__main__":
    if len(sys.argv) == 4:
        message = handle_input(sys.argv[2])
        codeword = handle_input(sys.argv[3])
        if sys.argv[1] == 'encode':
            result = playfair_e(codeword,message)
            print("encoded message: {}".format(result))
        elif sys.argv[1] == 'decode':
            result = playfair_d(codeword,message)
            print("decoded message: {}".format(result))
        else:
            print("invalid command action")
            print("python {} <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>".format(sys.argv[0]))
    else:
        print("invalid command format")
        print("python {} <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>".format(sys.argv[0]))