from cs50 import get_float


def main():
    dollars = 0
    while (dollars <= 0):
        try:
            dollars = get_float("Un nombre a virgule en dollard :")
        except:
            pass

    cents = int(round(dollars * 100))
    pieces = calculate_pieces(cents)
    print(pieces)


def calculate_pieces(cents):
    pieces_25 = cents // 25
    cents = cents % 25

    pieces_10 = cents // 10
    cents = cents % 10

    pieces_5 = cents // 5
    cents = cents % 5

    pieces_1 = cents

    pieces_total = pieces_25 + pieces_10 + pieces_5 + pieces_1
    return pieces_total


main()
