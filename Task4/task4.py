import heapq
import string
from collections import deque

def letter_swaps_generator(letters):
    swaps = []
    for i in range(len(letters)):
        for j in  range(i + 1, len(letters)):
            if ord(letters[i]) < ord(letters[j]):
                swaps.append(letters[i] + letters[j])
            else:
                swaps.append(letters[j] + letters[i])
    swaps.sort(key=lambda x: (x[0], x[1]))
    return swaps

# The swap function from task 1
def swap_letters(text, swap):
    swap_dict = {}
    for i in range(0, len(swap), 2):
        swap_dict[swap[i].lower()] = swap[i + 1].lower()
        swap_dict[swap[i].upper()] = swap[i + 1].upper()
        swap_dict[swap[i + 1].lower()] = swap[i].lower()
        swap_dict[swap[i + 1].upper()] = swap[i].upper()
        
    return ''.join([swap_dict.get(char, char) for char in text])


# Keep your code for reading message and dictionary
def load_words(filename):
    with open(filename, 'r') as f:
        words = [word.strip() for word in f.readlines()]
    return words

def check_words(words, dictionary, threshold):
    cleaned_words = [word.lower().translate(str.maketrans('', '', string.punctuation)) for word in words]
    percentage = sum(1 for word in cleaned_words if word in dictionary) / len(cleaned_words) * 100
    return percentage >= threshold

def search_algorithm(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    message_words = load_words(message_filename)
    dictionary = set(load_words(dictionary_filename))
    letter_swaps = letter_swaps_generator(letters)

    message = ' '.join(message_words)
    if algorithm == 'd': # check if algorithm is 'd'
        fringe = [(message, "", 0)] # use a stack instead of a queue
    else:
        fringe = deque([(message, "", 0)]) # use a queue for other algorithms
    max_fringe_size = len(fringe)
    expanded_nodes_count = 0
    max_search_depth = -1 # set max_search_depth to -1 instead of 0
    expanded_nodes = []

    visited_states = set() # create a set to store visited states

    while fringe:
        if algorithm == 'd': # check if algorithm is 'd'
            current_state, key_sequence, depth = fringe.pop() # use pop instead of popleft
        else:
            current_state, key_sequence, depth = fringe.popleft()
        expanded_nodes_count += 1
        if debug == 'y' and len(expanded_nodes) < 10:
            expanded_nodes.append(current_state)
            
        if check_words(current_state.split(), dictionary, threshold):
            return current_state, key_sequence, depth, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes
    
        # Remove the depth limit condition
        children = [(swap_letters(current_state, new_key), key_sequence + new_key, depth + 1) for new_key in letter_swaps]
        if algorithm == 'd': # check if algorithm is 'd'
            children.reverse() # reverse the order of the children
        for child in children:
            if child[0] not in visited_states: # check if the child state has been visited before
                if algorithm == 'd': # check if algorithm is 'd'
                    fringe.append(child) # use append instead of appendleft
                else:
                    fringe.appendleft(child)
                visited_states.add(child[0]) # add the child state to the visited set
        max_fringe_size = max(max_fringe_size, len(fringe))
        max_search_depth = max(max_search_depth, depth) # set max_search_depth to depth instead of depth + 1

    return 'No solution found.', None, None, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes

def task4(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    result = search_algorithm(algorithm, message_filename, dictionary_filename, threshold, letters, debug)
    
    if result[0] == 'No solution found.':
        output = f"No solution found.\n\n"
    else:
        output = f"Solution: {result[0]}\n\nKey: {result[1]}\nPath Cost: {result[2]}\n\n"

    output += f"Num nodes expanded: {result[3]}\nMax fringe size: {result[4]}\nMax depth: {result[5]}"
    
    if debug == 'y':
        output += "\n\nFirst few expanded states:\n" + '\n\n'.join(result[6])
    return output

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))