from enum import Enum

english_characters = "abcdefghijklmnopqrstuvwxyz"
key = "monarchy"

text = "attack"
cipher = ""
matrix = [[None for _ in range(5)] for _ in range(5)]
diagram = []
character_position = {}

class Relation(Enum):
    SAME_COL = 0
    SAME_ROW = 1
    NOT_SAME = 2

def play_fair():
    # fill key
    idx = fill_key()
    # fill the remaining
    fill_remaining(idx)

def fill_key():
    idx = 0
    for c in key:
        matrix[idx // 5][idx % 5] = c
        idx += 1
    return idx

def fill_remaining(idx):
    for c in english_characters:
        if c in key:
            continue
        if c == 'j' and 'i' not in key and 'j' not in key:
            matrix[(idx-1) // 5][(idx-1) % 5] = 'ij'
            continue
        matrix[idx // 5][idx % 5] = c
        idx += 1

def gen_diagram():
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'x'
        if a == b:
            diagram.append([a, 'x'])
            i += 1
        else:
            diagram.append([a, b])
            i += 2

def gen_hashmap():
    for i in range(5):
        for j in range(5):
            character_position[matrix[i][j]] = [i,j]

def encrypt():
    for pair in diagram:
        position = determine_position(pair)
        print(position)
        match position:
            case Relation.SAME_COL:
                move_down(pair)
            case Relation.SAME_ROW:
                move_right(pair)
            case Relation.NOT_SAME:
                swap(pair)

def determine_position(pair):
    first, second = get_pair_positions(pair)
    if first[0] == second[0]:
        return Relation.SAME_COL
    elif first[1] == second[1]:
        return Relation.SAME_ROW
    else:
        return Relation.NOT_SAME

def move_down(pair):
    global cipher
    first, second = get_pair_positions(pair)
    # Move each letter in the pair one column to the right (wrapping around if needed)
    first_row, first_col = first
    second_row, second_col = second
    first_new_char = matrix[first_row][(first_col + 1) % 5]
    second_new_char = matrix[second_row][(second_col + 1) % 5]
    cipher += first_new_char + second_new_char

def move_right(pair):
    global cipher
    first, second = get_pair_positions(pair)
    # Move each letter in the pair one row down (wrapping around if needed)
    first_row, first_col = first
    second_row, second_col = second
    first_new_char = matrix[(first_row + 1) % 5][first_col]
    second_new_char = matrix[(second_row + 1) % 5][second_col]
    cipher += first_new_char + second_new_char

def swap(pair):
    global cipher
    first, second = get_pair_positions(pair)
    first_row, first_col = first
    second_row, second_col = second
    cipher += matrix[first_row][second_col] + matrix[second_row][first_col]
    pass

def get_pair_positions(pair):
    return character_position[pair[0]], character_position[pair[1]]

play_fair()
gen_diagram()
gen_hashmap()
encrypt()
print(cipher)