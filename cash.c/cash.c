#include <cs50.h>
#include <stdio.h>

int calculate_pieces(int cents);

int main(void)
{
    // Prompt the user for change owed, in cents
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int pieces = calculate_pieces(cents);
    printf("%i\n", pieces);
}

int calculate_pieces(int cents)
{
    int pieces_25 = 0;
    while (cents >= 25)
    {
        pieces_25++;
        cents = cents - 25;
    }

    int pieces_10 = 0;
    while (cents >= 10)
    {
        pieces_10++;
        cents = cents - 10;
    }

    int pieces_5 = 0;
    while (cents >= 5)
    {
        pieces_5++;
        cents = cents - 5;
    }

    int pieces_1 = 0;
    while (cents >= 1)
    {
        pieces_1++;
        cents = cents - 1;
    }
    int pieces_total = pieces_25 + pieces_10 + pieces_5 + pieces_1;
    return pieces_total;
}
