import string
import heapq
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

def dfs_algorithm(message_filename, dictionary_filename, threshold, letters, debug):
    message = open(message_filename, 'r').read().strip()
    dictionary = set(load_words(dictionary_filename))
    letter_swaps = letter_swaps_generator(letters)
    stack = [(message, "", 0)]
    max_fringe_size = 1
    expanded_nodes_count = 0
    max_search_depth = -1
    expanded_nodes = []

    visited_states = set()

    while stack:
        current_state, key_sequence, depth = stack.pop()
        expanded_nodes_count += 1
        if expanded_nodes_count > 1000:
                return 'No solution found.', None, None, expanded_nodes_count - 1, max_fringe_size, max_search_depth, expanded_nodes
        
        if debug == 'y' and len(expanded_nodes) < 10:
            expanded_nodes.append(current_state)

        if check_words(current_state.split(), dictionary, threshold):
            return current_state, key_sequence, depth, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes

        if depth > max_search_depth:
            max_search_depth = depth

        children = [(swap_letters(current_state, new_key), key_sequence + new_key, depth + 1) for new_key in letter_swaps]
        children.reverse()
        for child in children:
            visited_states.add(child[0])
            stack.append(child)

        max_fringe_size = max(max_fringe_size, len(stack))

    return 'No solution found.', None, None, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes

def bfs_algorithm(message_filename, dictionary_filename, threshold, letters, debug):
    message = open(message_filename, 'r').read().strip()
    dictionary = set(load_words(dictionary_filename))
    letter_swaps = letter_swaps_generator(letters)
    queue = deque([(message, "", 0)])
    max_fringe_size = 1
    expanded_nodes_count = 0
    max_search_depth = -1
    expanded_nodes = []
    parent_nodes = {}
    
    while queue:
        current_state, key_sequence, depth = queue.popleft()
        expanded_nodes_count += 1
        if debug == 'y' and len(expanded_nodes) < 10:
            expanded_nodes.append(current_state)
        
        if check_words(current_state.split(), dictionary, threshold):
            # if the message is deciphered, construct the path from the root to the goal node
            path = []
            node = current_state
            while node != message:
                path.append(parent_nodes[node])
                node = parent_nodes[node]
                
            path.reverse()
            key_sequence = ''.join(path)
            return current_state, key_sequence, depth, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes
        
        if depth > max_search_depth:
            max_search_depth = depth
        
        children = [(swap_letters(current_state, new_key), new_key, depth + 1) for new_key in letter_swaps]
        for child in children:
            if child[0] not in parent_nodes:
                parent_nodes[child[0]] = child[1]
                queue.append(child)
                max_fringe_size = max(max_fringe_size, len(queue))
    
    return 'No solution found.', None, None, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes

def greedy_algorithm(message_filename, dictionary_filename, threshold, letters, debug):
    message = open(message_filename, 'r').read().strip()
    dictionary = set(load_words(dictionary_filename))
    letter_swaps = letter_swaps_generator(letters)
    heap = [(h(message, dictionary, threshold), message, [], 0, 0)]
    max_fringe_size = 1
    expanded_nodes_count = 0
    max_search_depth = -1
    expanded_nodes = []

    while heap:
        _, current_state, key_sequence, path_cost, depth = heapq.heappop(heap)
        expanded_nodes_count += 1
        if expanded_nodes_count > 1000:
            return 'No solution found.', None, None, expanded_nodes_count - 1, max_fringe_size, max_search_depth, expanded_nodes

        if debug == 'y' and len(expanded_nodes) < 10:
            expanded_nodes.append(current_state)

        if check_words(current_state.split(), dictionary, threshold):
            sorted_key_sequence = sorted(key_sequence)
            return current_state, ''.join(sorted_key_sequence), path_cost, expanded_nodes_count, max_fringe_size, depth, expanded_nodes

        max_search_depth = max(max_search_depth, depth)

        children = [(swap_letters(current_state, new_key), h(swap_letters(current_state, new_key), dictionary, threshold), key_sequence + [new_key], path_cost + 1, depth) for new_key in letter_swaps]
        children.sort(key=lambda x: x[1])
        for child in children:
            heapq.heappush(heap, (child[1], child[0], child[2], child[3], child[4]+1))

        max_fringe_size = max(max_fringe_size, len(heap))

    return 'No solution found.', None, None, expanded_nodes_count, max_fringe_size, depth, expanded_nodes

def astar_algorithm(message_filename, dictionary_filename, threshold, letters, debug):
    message = open(message_filename, 'r').read().strip()
    dictionary = set(load_words(dictionary_filename))
    letter_swaps = letter_swaps_generator(letters)
    heap = [(h(message, dictionary, threshold), message, [], 0, 0)]
    max_fringe_size = 1
    expanded_nodes_count = 0
    max_search_depth = -1
    expanded_nodes = []

    while heap:
        _, current_state, key_sequence, path_cost, depth = heapq.heappop(heap)
        expanded_nodes_count += 1
        if expanded_nodes_count > 1000:
            return 'No solution found.', None, None, expanded_nodes_count - 1, max_fringe_size, max_search_depth, expanded_nodes

        if debug == 'y' and len(expanded_nodes) < 10:
            expanded_nodes.append(current_state)

        if check_words(current_state.split(), dictionary, threshold):
            sorted_key_sequence = sorted(key_sequence)
            return current_state, ''.join(sorted_key_sequence), path_cost, expanded_nodes_count, max_fringe_size, max_search_depth + 1, expanded_nodes

        max_search_depth = max(max_search_depth, depth)

        children = [(swap_letters(current_state, new_key), h(swap_letters(current_state, new_key), dictionary, threshold), key_sequence + [new_key], path_cost + 1, depth+1) for new_key in letter_swaps]
        children.sort(key=lambda x: x[1])
        for child in children:
            heapq.heappush(heap, (child[1], child[0], child[2], child[3], child[4]))

        max_fringe_size = max(max_fringe_size, len(heap))

    return 'No solution found.', None, None, expanded_nodes_count, max_fringe_size, max_search_depth, expanded_nodes

def h(message, dictionary, threshold):
    cleaned_words = [word.lower().translate(str.maketrans('', '', string.punctuation)) for word in message.split()]
    return sum(1 for word in cleaned_words if word not in dictionary) / len(cleaned_words) * 100 - threshold

def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    if algorithm == 'g':
        result = greedy_algorithm(message_filename, dictionary_filename, threshold, letters, debug)
    elif algorithm == 'a':
        result = astar_algorithm(message_filename, dictionary_filename, threshold, letters, debug)

    if result[0] == 'No solution found.':
        output = f"No solution found.\n\n"
    else:
        output = f"Solution: {result[0]}\n\nKey: {result[1]}\nPath Cost: {result[2]}\n\n"

    output += f"Num nodes expanded: {result[3]}\nMax fringe size: {result[4]}\nMax depth: {result[5]}"
    
    if debug == 'y':
        output += "\n\nFirst few expanded states:\n" + '\n\n'.join(result[6])
    return output
    
if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task6 function
    print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))
    print(task6('a', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))
