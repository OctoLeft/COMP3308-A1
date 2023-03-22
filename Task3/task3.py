def load_words(filename):
    with open(filename, 'r') as f:
        words = [word.lower().strip() for word in f.readlines()]
        print(words)
    return words

def load_message_words(file_path):
    with open(file_path, 'r') as file:
        text = file.read().lower()
        words = []
        current_word = ""
        for character in text:
            if character.isalpha():
                current_word += character
            elif current_word:
                words.append(current_word)
                current_word = ""
        if current_word:
            words.append(current_word)
        print(words)
    return words

def task3(message_filename, dictionary_filename, threshold):
    message_words = load_message_words(message_filename)
    dictionary = set(load_words(dictionary_filename))

    correct_count = sum(word.lower() in dictionary for word in message_words)
    total_count = len(message_words)

    percentage_correct = (correct_count / total_count) * 100
    result = percentage_correct >= threshold

    return f"{result}\n{round(percentage_correct, 2):.2f}"

# Example usage:
print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
