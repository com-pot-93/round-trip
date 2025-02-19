import pandas as pd

def main_function(initial_field):
    for r in range(0,len(initial_field)):
        row = initial_field[r]
        for c in range(0,len(row)):
            curr_val = initial_field[r][c]
            if isinstance(curr_val, int):
                if curr_val != "":
                    print(curr_val)
                    if curr_val == 0:
                        initial_field = update_all_neighbours(temp,r,c,initial_field,'X')
                        main_function(initial_field)
                        break
                    else:
                        all_neighbours =  get_all_neighbours(temp,r,c,initial_field)
                        if '*' in all_neighbours:
                            bomb_neighbours = all_neighbours.count('*')
                            if bomb_neighbours == curr_val:
                                initial_field = update_all_neighbours(temp,r,c,initial_field,'X')
                                main_function(initial_field)
                                break
                            elif bomb_neighbours < curr_val:
                                left_neighbours = curr_val - bomb_neighbours
                                empty_neighbours = all_neighbours.count('')
                                if empty_neighbours == left_neighbours:
                                    initial_field = update_all_neighbours(temp,r,c,initial_field,'*')
                                    main_function(initial_field)
                                    break
                        else:
                            empty_neighbours = all_neighbours.count('')
                            if empty_neighbours == curr_val:
                                initial_field = update_all_neighbours(temp,r,c,initial_field,'*')
                                main_function(initial_field)
                                break
    return initial_field

def random_function(initial_field):
    for r in range(0,len(initial_field)):
        row = initial_field[r]
        for c in range(0,len(row)):
            curr_val = initial_field[r][c]
            if isinstance(curr_val, int):
                if curr_val != "":
                    print(curr_val)
                    all_neighbours =  get_all_neighbours(temp,r,c,initial_field)
                    if '*' in all_neighbours:
                        bomb_neighbours = all_neighbours.count('*')
                        if bomb_neighbours == curr_val:
                            initial_field = update_all_neighbours(temp,r,c,initial_field,'X')
                            main_function(initial_field)
                            break
                        elif bomb_neighbours < curr_val:
                            left_neighbours = curr_val - bomb_neighbours
                            empty_neighbours = all_neighbours.count('')
                            if empty_neighbours == left_neighbours:
                                initial_field = update_all_neighbours(temp,r,c,initial_field,'*')
                                main_function(initial_field)
                                break
                            elif empty_neighbours < left_neighbours:
                                print('conflict!!!!!!!!!!')
                        elif bomb_neighbours > curr_val:
                            print('conflict!!!!!')
                    else:
                        empty_neighbours = all_neighbours.count('')
                        if empty_neighbours == curr_val:
                            initial_field = update_all_neighbours(temp,r,c,initial_field,'*')
                            main_function(initial_field)
                            break
    return initial_field


temp = [-1,0,1]

def get_all_neighbours(temp,r,c,initial_field):
    all_neighbours = []
    for t in temp:
        for tt in temp:
            if t != 0 or tt != 0:
                if r+t != -1 and c+tt != -1:
                    try:
                        all_neighbours.append(initial_field[r+t][c+tt])
                    except:
                        pass
    return all_neighbours


def update_all_neighbours(temp,r,c,initial_field,symbol):
    for t in temp:
        for tt in temp:
            if t != 0 or tt != 0:
                if r+t != -1 and c+tt != -1:
                    try:
                        if initial_field[r+t][c+tt] == '':
                            initial_field[r+t][c+tt] = symbol
                    except:
                        pass
            else:
                initial_field[r+t][c+tt] = '{}!'.format(initial_field[r+t][c+tt])
    return initial_field




initial_field = [
[1, '','','','','','', 1, 1,'','','','','',''],
['','', 2,'', 2, 2,'','','', 2, 4, 3,'','', 0],
[ 0,'','','','','','', 2,'','','','','', 1,''],
['', 4,'','', 2,'', 2,'','','', 4, 3, 1,'',''],
['', 4,'','', 3,'','','','','','','','', 1,''],
['','', 6,'', 4,'','', 3, 4,'', 5,'','','',''],
[ 3, 4,'','','','', 3,'','','', 5,'','','',''],
['','', 5,'','','', 3, 5,'','','', 2,'', 3,''],
['','','', 3,'','', 2,'','','','', 0,'','', 4],
[ 3, 5,'','','', 3,'','','','', 1,'','','',''],
['', 3,'','','', 4,'','', 2,'', 3, 4,'','',''],
[ 3,'', 5,'', 6,'', 2, 2, 2, 2,'','','','', 1],
['','','','','','','', 2,'','', 3, 4, 3, 3,''],
[ 2, 2,'', 3,'','', 2,'','','','','','','', 1]
]

print(pd.DataFrame(initial_field))

main_function(initial_field)

print(pd.DataFrame(initial_field))





#['','','','','','','','','','','','','','',''],

