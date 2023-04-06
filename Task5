import math

def task5(message_filename, is_goal):
    with open(message_filename, 'r') as f:
        message = f.read().replace('\n', '').upper()
        
    if is_goal:
        return 0

    letter_counts = {
        'A': 0,
        'E': 0,
        'N': 0,
        'O': 0,
        'S': 0,
        'T': 0
    }

    for letter in message:
        if letter in letter_counts:
            letter_counts[letter] += 1

    def out_of_place(sorted_letters):
        return sum(1 for i, letter in enumerate(sorted_letters) if letter != 'ETAONS'[i])

    sorted_letters = sorted(letter_counts.items(), key=lambda x: (-x[1], x[0]))
    sorted_letters = ''.join([x[0] for x in sorted_letters])
    num_out_of_place = out_of_place(sorted_letters)

    return math.ceil(num_out_of_place / 2)


if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task5 function
    print(task5('freq_eg1.txt', False))
    print(task5('freq_eg1.txt', True))
    print(task5('freq_eg2.txt', False))
