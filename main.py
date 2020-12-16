import argparse
import matplotlib.pyplot as plt
import numpy as np
import time

descStr = "Conway's game of life:" \
       "Simulated by Python with randomized or user defined starting points"


def create_array(col_len, row_len):
    return np.array([0]*col_len*row_len)


def random_bin_array(K, N):
    arr = np.zeros(N)
    arr[:K] = 1
    np.random.shuffle(arr)
    return arr


def convert_coordinates(x,y,col_length):
    return y-1 - (x-1) * col_length


def extend_map(orig_array, col_length):
    # this function creates map with a border around it with opposing postions (like a pacman-field where each end
    extended_map = []
    # add each row with the end position in front and the first position at the end

    for i in range(0,col_length):
        row = [col_length * (i + 1) -1]
        row.extend(orig_array[col_length*i:(col_length*i+col_length)])
        row.append(orig_array[col_length * i])
        extended_map.append(row)
    # returns list in the form of [[row(n)], [row(1)]...[row(n-1)],[row(n)], [row(1)]]
    # adds the first row at the and, and likewise the last row in front
    extended_map.insert(len(extended_map),extended_map[0])
    extended_map.insert(0,extended_map[-2])

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
    for i in range(1,len(extended_list)-1):
        # i = column pos, j = row pos
        for j in range(1, len(extended_list[i])-1): #minus two, bc the first and last dont count
            above = extended_list[i-1][j-1:j+2]
            lr = [extended_list[i][j-1], extended_list[i][j+1]]
            below = extended_list[i+1][j-1:j+2]
            surr_pos_dict[str(extended_list[i][j])] = above + lr + below
    return surr_pos_dict


def update_field(index_pos,board, pos_dict:dict):
    # the board is a numpy array and the positions to get come from a dictionary
    index_pos = str(index_pos)
    surrounding = pos_dict[index_pos]
    # using a list to get positions is possible bc its a numpy array
    surrounding = board[surrounding]
    index_pos = int(index_pos)
    if board[index_pos] == 1 and 1 < np.count_nonzero(surrounding == 1) < 4:
        return 1
    elif board[index_pos] == 1:
        # the condition that the surrounding count has to be anything else than 2 or 3
        return 0
    # if surrounding.count(1) == 3
    if np.count_nonzero(surrounding == 1) == 3:
        # all dead cells with 3 live neighbors come to life. Bc the previous condition filtered all the
        # instances with live fields, this doesn't a statement to check for it.
        return 1
    else:
        # all dead fields which do not conform to the previous statement stay dead
        return 0


def create_matrix(array1d, col, row):
    twod_matrix = np.reshape(array1d, (row, col))
    return twod_matrix


def update_graph(graph_name, data):
    graph_name.matshow(data)
    plt.draw()
    plt.show()
    plt.pause(.1)


def main():
    parser = argparse.ArgumentParser(description=descStr)
    # lets user select boardsize
    parser.add_argument('-b', '--boardsize', type=int, default=(9, 9), required=False,
                        help="b: boardsize, m:If user selects manual the program asks for positions")
    # lets user input custom positions
    parser.add_argument('-m', '--manual', nargs=1, required=False,
                        help="m:If user selects manual the program asks for positions")
    args = parser.parse_args()

    PERCENTAGE_ALIVE = 0.25
    
    if args.boardsize:
        boardsize_arg = str(args.boardsize)
        boardsize_arg = boardsize_arg.split(",")
        col_len = int(boardsize_arg[0])
        row_len = int(boardsize_arg[1])
    else:
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
        board = random_bin_array(round(PERCENTAGE_ALIVE*total_size),total_size)

    pos_board = np.arange(len(board))
    border_map = extend_map(pos_board,col_len)
    pos_dict = dict_from_list(border_map)

    matrix = create_matrix(board, col_len, row_len)

    # First view of the board
    plt.ion()
    board_view = plt.figure()
    graph1 = board_view.add_subplot(111)
    graph1.matshow(matrix)
    plt.draw()
    plt.show()
    plt.pause(.1)

    while True:
        new_board = []
        for ix in range(len(board)):
            new_board = np.append(new_board,update_field(ix, board,pos_dict))
        board = new_board

        time.sleep(1)
        matrix = create_matrix(board, col_len, row_len)
        update_graph(graph1, matrix)


if __name__ == '__main__':
    main()