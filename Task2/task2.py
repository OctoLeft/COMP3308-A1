def letter_swaps_generator(letters):
    swaps = []
    for i in range(len(letters)):
        for j in  range(i + 1, len(letters)):
            if ord(letters[i]) < ord(letters[j]):
                swaps.append(letters[i] + letters[j])
            else:
                swaps.append(letters[j] + letters[i])
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

def task2(filename, letters):
    with open(filename, 'r') as f:
        text = f.read()

    swaps = letter_swaps_generator(letters)
    swaps.sort(key=lambda x: (x[0], x[1]))
    new_text = [swap_letters(text, swap) for swap in swaps]

    # Check and make sure the new text is not the same as the original
    new_text = [char for char in new_text if char != text]

    # No \n needed if len is 0
    if len(new_text) == 0:
        return "0"

    return f"{len(new_text)}\n" + "\n\n".join(new_text)

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task2 function
    # print(task2('spain.txt', 'ABE'))
    # print(task2('ai.txt', 'XZ'))
    # print(task2('cabs.txt', 'ABZD'))
    print(task2('king.txt', 'MLKJ'))