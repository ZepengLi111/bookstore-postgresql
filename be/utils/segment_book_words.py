import jieba

stops = [
    "―",
    "“",
    "”",
    "。",
    "    ",
    ".",
    "'",
    "，",
    "\n",
    "]",
    "[",
    "·",
    "(",
    ")",
    "（",
    "）",
    "；",
    "...",
    "......",
    ",",
    "《",
    "》",
    "—",
    "、",
    "・",
    "",
    
]

def cut_word(text) -> list:
    words = jieba.cut(str(text))
    words = [word.strip() for word in words if word.strip() not in stops]
    return words

def generate_book_kwords(book_dict) -> str:
    kwords = []
    attributes = ['title', 'author', 'tags', 'author_intro', 'book_intro', 'content']
    for attribute in attributes:
        text = book_dict[attribute]
        if text != None:
            words = cut_word(text)
            kwords.extend(words)
    return " ".join(kwords)


