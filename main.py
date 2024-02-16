import copy
import random
import os
import math

# Creates 3 lists with a random number of elements between 2 and 6 and puts them into a list init_heaps.
def initial_state():
    init_heaps = []
    for i in range(0, 3):
        num_elements = random.randint(2, 6)
        curr_heap = []
        for j in range(0, num_elements):
            curr_heap.append((i, j))
        init_heaps.append(curr_heap)
    return init_heaps

def load_file(heaps, input_file):
    # A check should be made first if input_file exists by the calling function, so it's assumed that the file exists. If the found file is empty, however, do not update the heaps.
    if os.stat('input.txt').st_size == 0:
        print('load_file(): Empty input.txt found. Not updating heaps.')
        return
    
    # Clear each heap in heaps and reset it.
    for heap in heaps:
        heap.clear()

    # Read the lines from the file into a list.
    input_lines = input_file.readlines()
    # Iterate through each line to extract elements and store them into the heaps.
    for line_idx in range(0, len(input_lines)):
        # Take out the newline character from the current line in question.
        curr_line = input_lines[line_idx].replace('\n', '')
        # Variable used to keep track of what number valid element is being added to the heap in the case of invalid characters or whitespace.
        num_elements = 0
        # Iterate through each character in the line. For each "I" found, add a coordinate to the corresponding heap.
        for curr_char in curr_line:
            if curr_char == 'I':
                heaps[line_idx].append((line_idx, num_elements))
                num_elements += 1

def player(current_player):
    if current_player == 1:
        return 2
    elif current_player == 2:
        return 1
    else:
        return -1
    
def actions(heaps):
    possible_actions = []

    for heap_idx in range(0, len(heaps)):
        match heap_idx:
            case 0:
                heap_letter = 'A'
            case 1:
                heap_letter = 'B'
            case 2:
                heap_letter = 'C'
        curr_heap = list.copy(heaps[heap_idx])
        while len(curr_heap) > 0:
            possible_actions.append((heap_letter, len(curr_heap)))
            curr_heap.pop()
    
    # print(f'actions(): possible_actions:')
    # [print(action) for action in possible_actions]
    # print(f'actions(): possible_actions: {possible_actions}')
    
    return possible_actions

# Made up terminal since it wasn't defined in the notes. If there are no more moves left to make for the heaps, then return True. If there are moves, return False.
def terminal(heaps, current_player):
    # If there are no more actions to be taken or a player has already won, then return True.
    if len(actions(heaps)) == 0 or winner(heaps, current_player) != None:
        return True
    
    return False
    

def result(heaps, action):
    # if len(action) != 2:
    #     raise Exception("result function: incorrect action")
    # if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
    #     raise Exception("result function: incorrect action value")
    
    y, x = str(action[0]), int(action[1])

    match y:
        case 'A':
            heap_idx = 0
        case 'B':
            heap_idx = 1
        case 'C':
            heap_idx = 2

    heaps_copy = copy.deepcopy(heaps)

    if len(heaps_copy[heap_idx]) == 0:
        raise Exception('heap is already empty.')
    else:
        heaps_copy[heap_idx] = [heaps_copy[heap_idx][element_idx] for element_idx in range(0, len(heaps_copy[heap_idx]) - x)]
        # print(f'result(): heaps_copy[{heap_idx}] after action: {heaps_copy[heap_idx]}')

    return heaps_copy

def winner(heaps, current_player):
    # If all of the heaps are empty, then the current player must have been the one to have took the last piece algorithmically. Return the opposite player as the winner.
    if len(heaps[0]) == 0 and len(heaps[1]) == 0 and len(heaps[2]) == 0:
        return player(current_player)
    # Otherwise, there is no winner
    return None

def utility(heaps, current_player):
    print(f'utility(): winner(heaps, current_player): {winner(heaps, current_player)}')
    print_heaps(heaps)
    if winner(heaps, current_player) == 1:
        return 1
    elif winner(heaps, current_player) == 2:
        return -1
    else:
        return 0
    
def minimax(heaps, current_player):
    # print(f'minimax(): terminal: {terminal(heaps, current_player)}')
    if terminal(heaps, current_player):
        return None
    
    if player(current_player) == 2:
        score = -math.inf
        action_to_take = None

        for action in actions(heaps):
            min_val = minvalue(result(heaps, action), 0, current_player)
            if min_val > score:
                score = min_val
                action_to_take = action

        return action_to_take
    # CPU should take this route.
    elif player(current_player) == 1:
        score = math.inf
        action_to_take = None

        for action in actions(heaps):
            max_val = maxvalue(result(heaps, action), 0, current_player)
            print(f'minimax(): max_val: {max_val}, action: {action}')
            if max_val < score:
                score = max_val
                action_to_take = action

        return action_to_take
    
def minvalue(heaps, depth, current_player):
    if terminal(heaps, current_player):
        if (depth % 2) > 0:
            match current_player:
                case 1:
                    return 1
                case 2:
                    return -1
        else:
            match current_player:
                case 1:
                    return -1
                case 2:
                    return 1
    
    # Iterate over the available actions and return the minimum out of all maximums
    max_value = math.inf
    for action in actions(heaps):
        max_value = min(max_value, maxvalue(result(heaps, action), depth + 1, current_player))
    
    return max_value

def maxvalue(heaps, depth, current_player):
    if terminal(heaps, current_player):
        if (depth % 2) > 0:
            match current_player:
                case 1:
                    return 1
                case 2:
                    return -1
        else:
            match current_player:
                case 1:
                    return -1
                case 2:
                    return 1
    
    min_val = -math.inf
    for action in actions(heaps):
        min_val = max(min_val, minvalue(result(heaps, action), depth + 1, current_player))

    return min_val

def print_heaps(heaps):
    for row_idx in range(0, len(heaps)):
        match row_idx:
            case 0:
                row_letter = 'A'
            case 1:
                row_letter = 'B'
            case 2:
                row_letter = 'C'
        print(f'Heap {row_letter}:', "".join(['I' for elements in heaps[row_idx]]), '->', " ".join(str(coordinates) for coordinates in heaps[row_idx]))

def parse_action(action, heaps):
    action_letter, action_num_elements = str(action[0]), int(action[1])
    match action_letter:
        case 'A':
            heap_idx = 0
        case 'B':
            heap_idx = 1
        case 'C':
            heap_idx = 2
    return [(heap_idx, element) for element in range(len(heaps[heap_idx]) - action_num_elements, len(heaps[heap_idx]))]

def main():
    heaps = initial_state()

    # Open input file if it exists.
    if os.path.exists('input.txt'):
        print('main(): input.txt found! Loading from file...')
        input_file = open('input.txt', 'r')
        # Load from file and update heaps.
        load_file(heaps, input_file)
    else:
        print('main(): input.txt not found. Starting with empty heaps...')

    print('_____________________________________________')
    print("Welcome to Tao!")
    print("Player #1 goes first.")

    output_file = open('output.txt', 'w')

    # Algorithmically, current_player needs to start at 2 so that the first to play will be Player #1.
    current_player = 2
    prev_move_valid = True
    # Let the Players take their turns until completion.
    while not terminal(heaps, current_player):
        print_heaps(heaps)
        if prev_move_valid:
            current_player = player(current_player)

        print(f"Player #{current_player}'s turn:")

        if current_player == 1:
            x, y = map(str, input("Enter your move (row and column): ").split())
            action = (x.upper(), int(y))
            print(f'main(): action inputted: {action}')
        else:
            action = minimax(heaps, current_player)
            print(f'main(): CPU action: {action}')
            
        if action not in actions(heaps):
            print("Invalid move. Try again.")
            prev_move_valid = False
        else:
            prev_move_valid = True
            output_file.write(f'player#{current_player}: ' + ", ".join(str(element).replace(" ", "") for element in parse_action(action, heaps)) + '\n')
            heaps = result(heaps, action)

    print_heaps(heaps)
    game_winner = winner(heaps, current_player)

    if game_winner is None:
        print("It's a draw!")
        output_file.write('winner: draw')
    else:
        print(f"Player #{game_winner} wins!")
        output_file.write(f'winner: player#{game_winner}')

    output_file.close()

main()