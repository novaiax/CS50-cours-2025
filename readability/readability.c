#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text:");

    // calcul du nombre de lettre dans le text
    int letters = count_letters(text);

    // calcul du nombre de mots dans le text
    int words = count_words(text);

    // calcul du nombre de phrase (commencant par majuscul et terminant par un point) dans le text
    int sentences = count_sentences(text);

    // formule application pour calculer le niveau : index = 0.0588 * L - 0.296 * S - 15.8
    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    // afficher le level

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

// calcul du nombre de lettre dans le text
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    // isalpha - vérifier si un caractère est alphabétique
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}

// calcul du nombre de mots dans le text
int count_words(string text)
{
    int words = 1;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
    }
    return words;
}

// calcul du nombre de phrase (commencant par majuscul et terminant par un point) dans le text
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }
    return sentences;
}
