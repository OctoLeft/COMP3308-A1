# The load dictionary function from Task 3
def load_words(filename):
    with open(filename, 'r') as f:
        words = [word.strip() for word in f.readlines()]
        print(words)
    return words

# The letter swaps generator function from Task 2
def letter_swaps_generator(letters):
    swaps = []
    for i in range(len(letters)):
        for j in  range(i + 1, len(letters)):
            if ord(letters[i]) < ord(letters[j]):
                swaps.append(letters[i] + letters[j])
            else:
                swaps.append(letters[j] + letters[i])
    return swaps

# The swap letters function from Task 1
def swap_letters(text, swap):
    swap_dict = {}
    for i in range(0, len(swap), 2):
        swap_dict[swap[i].lower()] = swap[i + 1].lower()
        swap_dict[swap[i].upper()] = swap[i + 1].upper()
        swap_dict[swap[i + 1].lower()] = swap[i].lower()
        swap_dict[swap[i + 1].upper()] = swap[i].upper()
        
    return ''.join([swap_dict.get(char, char) for char in text])

def generate_children(state, allowed_swaps):
    children = []
    swaps = letter_swaps_generator(allowed_swaps)
    for swap in swaps:
        child = swap_letters(state, swap)
        children.append(child)
    return children

def goal_check(state, dictionary, threshold):
    words = state.split()
    valid_words = sum(1 for word in words if word.lower() in dictionary)
    valid_words_percentage = valid_words / len(words) * 100
    return valid_words_percentage >= threshold

def depth_first_search(start_state, dictionary, allowed_swaps, threshold):
    stack = [start_state]
    visited = set()
    while stack:
        state = stack.pop()
        if goal_check(state, dictionary, threshold):
            return state
        if state not in visited:
            visited.add(state)
            children = generate_children(state, allowed_swaps)
            stack.extend(children)
    return None

def task4(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    message_words, dictionary_words = load_words(message_filename), load_words(dictionary_filename)

    

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    # print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    # print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    # print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))