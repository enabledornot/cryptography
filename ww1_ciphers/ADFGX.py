import sys
import itertools
from tools import *
keylist = ['A','D','F','G','X']
def adfgx_translate_e(char,grid):
    row, column = grid.row_column(char)
    return keylist[row] + keylist[column]
def adfgx_codewordify(message, codeword):
    message_cw = []
    len_cw = len(codeword)
    for i in range(len_cw):
        message_cw.append((codeword[i],[]))
    for i,c in enumerate(message):
        message_cw[i % len_cw][1].append(c)
    return message_cw
def adfgx_decodewordify(message):
    message_dcw = ""
    for column in message:
        message_dcw += "".join(column[1])
    return message_dcw
def adfgx_e(codegrid, codeword, d_message):
    grid = Polybius(codegrid)
    e_message = ""
    for char in clean_text(d_message):
        e_message += adfgx_translate_e(char, grid)
    e_message_cw = adfgx_codewordify(e_message, codeword)
    e_message_cw.sort(key=lambda x: x[0])
    return adfgx_decodewordify(e_message_cw)
def adfgx_translate_d(chars,grid):
    row = keylist.index(chars[0])
    column = keylist.index(chars[1])
    return grid.get(row, column)
def array_slice(ary, slices):
    ary_c = ary.copy()
    sliced_ary = [[]]
    while len(ary_c) != 0:
        if slices[0] == 0:
            slices.pop(0)
            if len(slices) == 0:
                break
            sliced_ary.append([])
        slices[0] -= 1
        sliced_ary[-1].append(ary_c.pop(0))
    return sliced_ary
def adfgx_undecodewordify(e_message, codeword):
    codeword = list(codeword)
    sorted_cw = sorted(codeword)
    slice_map = []
    lower_grid_height = len(message) // len(codeword)
    height_change_point = len(message) % len(codeword)
    for cw_c in sorted_cw:
        if height_change_point > codeword.index(cw_c):
            slice_map.append(lower_grid_height + 1)
        else:
            slice_map.append(lower_grid_height)
    e_message_cw = []
    for i, column in enumerate(array_slice(list(e_message),slice_map)):
        e_message_cw.append((sorted_cw[i], column))
    return e_message_cw
def adfgx_uncodewordify(e_message_cw):
    e_message = ""
    index = 0
    done = False
    while not done:
        for column in e_message_cw:
            if len(column[1]) <= index:
                done = True
                break
            e_message+=column[1][index]
        index += 1
    return e_message
def adfgx_d(codegrid, codeword, e_message):
    grid = Polybius(codegrid)
    codeword_l = list(codeword)
    # encrypted message codeword unsorted
    e_message_cw_u = adfgx_undecodewordify(e_message, codeword_l)
    e_message_cw_s = [()]*len(codeword)
    # unscramble word that hopefully has unique chars
    # if not first char goes to first char in word
    for column in e_message_cw_u:
        letter_index = codeword_l.index(column[0])
        codeword_l[letter_index] = "_"
        e_message_cw_s[letter_index] = column
    e_message = adfgx_uncodewordify(e_message_cw_s)
    d_message = ""
    for segment in split_segment(e_message,2):
        d_message += adfgx_translate_d(segment, grid)
    return d_message
if __name__ == "__main__":
    if len(sys.argv) == 5:
        message = handle_input(sys.argv[2])
        codegrid = handle_input(sys.argv[3])
        codeword = handle_input(sys.argv[4])
        if sys.argv[1] == 'encode':
            result = adfgx_e(codegrid,codeword,message)
            print("encoded message: {}".format(result))
        elif sys.argv[1] == 'decode':
            result = adfgx_d(codegrid,codeword,message)
            print("decoded message: {}".format(result))
        else:
            print("invalid command action")
            print("python {} <encode:decode> <message_or_filename_of_message> <codegrid_or_filename_of_codegrid> <codeword_or_filename_of_codeword>".format(sys.argv[0]))
    else:
        print("invalid command format")
        print("python {} <encode:decode> <message_or_filename_of_message> <codegrid_or_filename_of_codegrid> <codeword_or_filename_of_codeword>".format(sys.argv[0]))