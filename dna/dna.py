import csv
import sys


def main():

    # 1. Vérifier les arguments de ligne de commande

    # 2. Ouvrir et lire le CSV dans une liste de dictionnaires

    # 3. Ouvrir et lire la séquence ADN dans une string

    # 4. Pour chaque STR → appliquer longest_match

"""
ouvrir le csv file et la sequence dna et lire son contenu dans la mémoire

pour chaque STR, on va calculer la  plus longue sequence de répeitions qui s'enchaine de ce STR pour dans la sequence DNA fournie

Comparer le nombres de STR avec chaque ligne du csv.file pour rechercher une correspondanc, si il y a une correspondance, print name ect et sinon no match (aucune correspondance)
"""


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
