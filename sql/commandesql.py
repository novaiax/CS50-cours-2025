import sqlite3
import csv
sqlite3()
csv()

#importer csv

terminal :
    .modde csv
    .imporrt fichier.csv table (cela creer un nouveau fichier appeler "Table.db")
    .schema (voir ce tous ce qu'il y a dans cette base)

commande :

    #(selectionner la colonne d'une table) (possibilité d'utiliser "*" si on veut selectionner toutes les colonnes de la table)
    terminal sqlite> SELECT colonnes FROM table;

    #utiliser une fonction : AVG / Count / DISTINCT / LOWER / MAX / MIN / UPPER
    terminal sqlite> SELECT FONCTION(colonne) FROM table;

    1er exemple : SELECT COUNT(*) FROM favorites;

    2eme exemple : SELECT DISTINCT colonne FROM favorites; #Les parenthese sont pas toujours nécéssaire

    3eme exemple : SELECT COUNT(DISTINCT language) FROM favorites;

    #Autres fonctionnalités :
    - GROUP BY
    - LIKE
    - LIMIT
    - ORDER BY
    - WHERE
    - ...

    1er exemple : SELECT COUNT(*) FROM favorites WHERE language = 'C';

    #utilisation de ORDER BY
    SELECT langugage, COUNT(*) FROM favorites GROUP BY language ORDER BY COUNT(*) ASC; #ascending order (ordre croissant)

    SELECT langugage, COUNT(*) FROM favorites GROUP BY language ORDER BY COUNT(*) DESC; #descending order (ordre décroissant)


    #On va rechercher tous les problemes qui commencent par H-E-L-L-O
    2eme exemple : SELECT COUNT(*) FROM favorites WHERE language = 'C'AND probleme LIKE 'HELLO, %';

    #utilisation de AND

    1er exemple : SELECT count(*) FROM favorites WHERE language = 'C' AND problem = 'HELLO, World';


