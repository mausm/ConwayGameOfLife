descStr = "Conway's game of life:" \
       "Simulated by Python with predetermined or user defined starting points"

import numpy as np
import matplotlib.pyplot as plt
import argparse


#TODO:
# ARGParse: let the user choose between: set the starting points or random points
# IF choosen use a method to set up the board
# DONE Build the board
# DONE Populate the board (1 is on, 0 is off)
# Method that updates the board on set of rules and repopulates the board
# DONE Write the conway set of rules


def create_array(col_len, row_len):
    return np.array([0]*col_len*row_len)


def random_bin_array(K, N):
    arr = np.zeros(N)
    arr[:K] = 1
    np.random.shuffle(arr)
    return arr


def convert_coordinates(x,y,col_length):
    return y-1 - (x-1) * col_length

# lets create a dictionary of surrounding index positions for each item in the list, so you can quickly check them later with numpy
# a = np.arry[list items]
# b = [1, 2, 5]
# list(a[b])


def extend_map(orig_array, col_length):
    # this function creates map with a border around it with opposing postions (like a pacman-field where each end
    extended_map = []
    # the row above the map
    extended_map.append([len(orig_array)] + orig_array[-col_length:] + orig_array[-col_length])
    # add each row with the end position in front and the first position at the end
    for i in range(0,len(orig_array // col_length)):
        row = [col_length * i] + orig_array[col_length*i:(col_length*i-1)] + orig_array[col_length * i + col_length -1]
        extended_map.append(row)
    extended_map.append([col_length] + orig_array[-col_length:] + orig_array[-col_length])
    # returns list in the form of [[row(n)], [row(1)]...[row(n-1)],[row(n)], [row(1)]]
    return extended_map


def dict_from_list(extended_list:list):
    # create a dictionary for each position with the surrounding 8 positions, so it can be referenced quickly
    """for example a 3*3 board 0-8 looks like this:
    [[8,6,7,8,6],
     [2,0,1,2,0],
     [5,3,4,5,3],
     [8,6,7,8,6],
     [2,0,1,2,0]]

    the first/last column is are the values from the opposite column
    the first/last row include the values from the opposite row

    now we can easily take the surrounding positions and put them into a dictionary. Like {1:[6,7,8,0,1,3,4,5]}
    """

    surr_pos_dict = dict()
    for row in extended_list[1:-1]:
        for value in row[1:-1]:
            above = [extended_list[row-1][value-1:value+1]]
            lr = [extended_list[row][value-1],extended_list[row][value+1]]
            below = [extended_list[row+1][value-1:value+1]]
            surr_pos_dict[str(value)] = above + lr + below

    return surr_pos_dict


def update_field(index_pos:int,board, pos_dict:dict):
    # the board is a numpy array and the posi tions to get come from a dictionary
    surrounding = pos_dict[i]
    # using a list to get positions is possible bc its a numpy array
    surrounding = board[surrounding]
    if board[index_pos] == 1 and 1 < surrounding.count(1) < 4:
        return 1
    elif board[index_pos] == 1:
        # the condition that the surrounding count has to be anything else than 2 or 3
        return 0
    if surrounding.count(1) == 3:
        # all dead cells with 3 live neighbors come to life. Bc the previous condition filtered all the
        # instances with live fields, this doesn't a statement to check for it.
        return 1
    else:
        # all dead fields which do not conform to the previous statement stay dead
        return 0


def main():

    parser = argparse.ArgumentParser(description=descStr)
    # lets user select boardsize
    parser.add_argument('b', '--boardsize', type=int, default=(9, 9), required=False,
                        help="b: boardsize, m:If user selects manual the program asks for positions")
    # lets user input custom positions
    parser.add_argument('m', '--manual', nargs=1, required=False,
                        help="m:If user selects manual the program asks for positions")
    args = parser.parse_args()

    PERCENTAGE_ALIVE = 0.25
    col_len, row_len = args.boardsize
    total_size = col_len * row_len

    if args.manual:
        on_positions = []
        while True:
            x, y = input("Please add an (x,y) position that should be on in form of 'x,y': ")
            try:
                x, y = int(x), int(y)
                if 0 < x <= args.boardsize[0] and 0 < y <= args.boardsize[1]:
                    on_positions.append((x, y))

            except ValueError:
                if input("please try again with a valid number, or press 'q' to quit: ") == 'q':
                    break

        board = np.zeros(total_size)
        for item in on_positions:
            i = convert_coordinates(item[0], item[1], col_len)
            board[i] = 1
    else:
        board = random_bin_array(PERCENTAGE_ALIVE*total_size,total_size)