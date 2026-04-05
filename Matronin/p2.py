from urllib.parse import unquote
import pyperclip

url_encoded = input('\nЗакодоване посилання: ')

url_decoded = unquote(url_encoded)

print('\nДекодоване посилання:')
print(url_decoded)

pyperclip.copy(url_decoded)
print('\nПосилання скопійовано в буфер обміну')