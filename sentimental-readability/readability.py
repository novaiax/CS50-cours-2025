import cs50


def main():
    text = cs50.get_string("Text : ")

    count_letters = count_letters_def(text)
    print(f"Nombre de lettres : {count_letters}")

    count_words = count_words_def(text)
    print(f"Nombre de mots : {count_words}")

    count_sentences = count_sentences_def(text)
    print(f"Nombre de phrase: {count_sentences}")

    # formule pour appliquer le niveau : 0.0588 * L - 0.296 * S - 15.8
    L = float((count_letters / count_words) * 100)
    S = float((count_sentences / count_words) * 100)

    index = float(0.0588 * L - 0.296 * S - 15.8)

    # afficher le level
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print("Grade :", int(round(index)))


# calcul du nombre de lettre dans le text
def count_letters_def(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    return letters


# calcul du nombre de mots dans le text
def count_words_def(text):
    words = 1
    for i in range(len(text)):
        if text[i].isspace():
            words += 1
    return words


def count_sentences_def(text):
    nb_sentences = 0
    for c in text:
        if c in ".!?":
            nb_sentences += 1
    return nb_sentences


main()
