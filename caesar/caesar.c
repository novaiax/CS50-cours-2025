#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ciphertext(string plaintext, int key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key is not valid\n");
        return 1;
    }
    int len = strlen(argv[1]);
    for (int i = 0; i < len; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key is not valid\n");
            return 1;
        }
    }
    string plaintext = get_string("plaintext: ");
    int key = atoi(argv[1]) % 26;
    printf("ciphertext: ");
    ciphertext(plaintext, key);
    printf("\n");
    return 0;
}

void ciphertext(string plaintext, int key)
{
    int len = strlen(plaintext);
    for (int i = 0; i < len; i++)
    {

        // si c’est une lettre minuscule, décaler à partir de 'a'
        //  islower vérifier si un caractère est en minuscule
        if (islower(plaintext[i]))
        {
            int index = plaintext[i] - 'a';
            int new_position = (index + key) % 26;
            int val = 'a' + new_position;
            printf("%c", val);
        }

        // si c’est une lettre majuscule, décaler à partir de 'A'
        // isupper vérifier si un caractère est en majuscule
        else if (isupper(plaintext[i]))
        {
            int index = plaintext[i] - 'A';
            int new_position = (index + key) % 26;
            int val = 'A' + new_position;
            printf("%c", val);
        }

        // si c'est un chiffre, ou ponctuation ou atre, on ne fait rien
        // ispunct vérifier si un caractère est une ponctuation
        // isspace vérifier si un caractère est un espace (par exemple, une nouvelle ligne, un
        // espace ou une tabulation) ispunct vérifier si un caractère est une ponctuation
        else
        {
            printf("%c", plaintext[i]);
        }
        // changer les mots en 26 (exemple 52 : on décale 0, 28 : on décale de 2 (car 26 x 1 + 2)
    }
}
