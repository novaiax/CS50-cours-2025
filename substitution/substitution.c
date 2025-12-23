#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ciphertext(string plaintext, string key);

int letters[26] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./sub key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Usage: ./sub key is not valid\n");
        return 1;
    }

    int len = strlen(argv[1]);
    for (int i = 0; i < len; i++)
    {
        char maj = toupper(argv[1][i]);
        int index = (maj) - 'A';
        if (!isalpha(argv[1][i]))
        {
            printf("Usage: ./sub key is not valid\n");
            return 1;
        }
        else if (letters[index] == 1)
        {
            printf("Usage: ./sub key is not valid\n");
            return 1;
        }
        else
        {
            letters[index] = 1;
        }
    }
    string plaintext = get_string("plaintext: ");
    string key = argv[1];
    printf("ciphertext: ");
    ciphertext(plaintext, key);
    printf("\n");
    return 0;
}

// NQXPOMAFTRHLZGECYJIUWSKDVB

void ciphertext(string plaintext, string key)
{
    // Transformer chaque lettre de la phrase en la lettre de la key (en fonction de la position
    // dans letters[26])

    // On parcourt chaque lettre de la chaine
    int len = strlen(plaintext);
    for (int i = 0; i < len; i++)
    {
        if (islower(plaintext[i]))
        {
            int index = plaintext[i] - 'a';
            printf("%c", tolower(key[index]));
        }
        else if (isupper(plaintext[i]))
        {
            int index = plaintext[i] - 'A';
            printf("%c", toupper(key[index]));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
}
