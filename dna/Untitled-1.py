
def main():

    # 1. Vérifier les arguments de ligne de commande
    if len(sys.argv) != 3:
        print("Error, Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # 2. Ouvrir et lire le CSV dans une liste de dictionnaires
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames[1:]
        database = []

    # 3. Ouvrir et lire la séquence ADN dans une string
        for row in reader:
            for str in strs:
                row[str] = int(row[str])
            database.append(row)

    with open(sys.argv[2]) as file:
            sequence = file.read()

    # 4. Pour chaque STR → appliquer longest_match
    counts = {}
    for str in strs:
        counts[str] = longest_match(sequence, str)

    for person in database:
        match = True
        for str in strs:
            if person[str] != counts[str]:
                match = False
                break
        if match:
            print(person["name"])
            return
    else:
        print("No match")
