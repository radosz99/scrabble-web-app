def read_words():
    words = open('resources/wordsPL.txt', "r",encoding='utf-8')
    return [line.strip().lower() for line in words]

def make_trie():
    words = read_words()
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root