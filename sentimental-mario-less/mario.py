def main():
    height = 0
    while (height < 1 or height > 8):
        try:
            height = int(input("La hauteur de la piramide entier entre 1 et 8 :"))
        except:
            pass

    for i in range(height):
        nb_espace = height - 1 - i
        nb_hashes = i + 1
        print_row(nb_hashes, nb_espace)


def print_row(nb_hashes, nb_espace):
    print(" " * nb_espace + "#" * nb_hashes)


main()
