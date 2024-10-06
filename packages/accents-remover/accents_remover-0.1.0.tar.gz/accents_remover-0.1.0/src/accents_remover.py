# %%
convert_list = {
    'à': {'replacer':'a'},
    'ã': {'replacer':'a'},
    'ä': {'replacer':'a'},
    'â': {'replacer':'a'},
    'á': {'replacer':'a'},
    'è': {'replacer':'e'},
    'é': {'replacer':'e'},
    'ê': {'replacer':'e'},
    'ë': {'replacer':'e'},
    'í': {'replacer':'i'},
    'ì': {'replacer':'i'},
    'î': {'replacer':'i'},
    'ï': {'replacer':'i'},
    'ï': {'replacer':'i'},
    'ò': {'replacer':'o'},
    'ó': {'replacer':'o'},
    'ô': {'replacer':'o'},
    'õ': {'replacer':'o'},
    'ö': {'replacer':'o'},
    'ù': {'replacer':'u'},
    'ú': {'replacer':'u'},
    'û': {'replacer':'u'},
    'ü': {'replacer':'u'},
    'ç': {'replacer':'c'},
    'ñ': {'replacer':'n'}}
# %%

def letter_replacer(letter):
    if letter in convert_list:
        return letter.replace(letter, convert_list[letter]['replacer'])
    return letter

def remove_accents(word: str):
    for letter in word:
        lower_letter = letter.lower()
        new_letter = letter_replacer(lower_letter)

        if letter.isupper():
            new_letter = new_letter.upper()
            
        word = word.replace(letter, new_letter)
    return word
