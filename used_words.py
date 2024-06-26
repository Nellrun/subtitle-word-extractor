import os

def load_used_words(file_path='used_words.txt'):
    if not os.path.exists(file_path):
        return set()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        used_words = set(file.read().splitlines())
    
    return used_words


used_words = load_used_words()

