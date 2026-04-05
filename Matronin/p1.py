def sort_key(word):
    ukr_alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    first_char = word[0].lower()

    if first_char in ukr_alphabet:
        group = 0
        char_keys = tuple(
            ukr_alphabet.index(c) if c in ukr_alphabet else 999
            for c in word.lower()
        )
    else:
        group = 1
        char_keys = tuple(ord(c) for c in word.lower())

    return (group, char_keys)

with open('text.txt', 'r', encoding='utf-8') as file:
    content = file.read()

print('\nПочатковий текст:')
print(content)

clean = content.replace('.', '').replace(',', '')
words = content.split()

print('\nСписок слів:')
print(words)

words.sort(key=sort_key)

print('\nВідсортований список:')
print(words)