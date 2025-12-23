#include <stdio.h>
#include <cs50.h>

void print_row(int nb_espace, int nb_hashes);

int main(void)
{
    int height;
    do
    {
        // demande la taille height
        height = get_int("Quel est la taille de la piramide ?");
    }
    while (height < 1);


    for (int i = 0; i < height; i++)
    {
        int nb_hashes = height - 1;
        int nb_espace = height - i;
        print_row(nb_espace, nb_hashes);
    }
}


void print_row(int nb_espace, int nb_hashes)
{
    for (int i = 0; i < nb_espace; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < nb_hashes; i++)
    {
        printf("#");
    }
    printf("\n");
}
