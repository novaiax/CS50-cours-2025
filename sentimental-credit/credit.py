from cs50 import get_int, get_string
#demander 15 chiffres (donc 15 caracteres obligoire sinon invalide)

def main():
    num = input("Numero de carte bancaire (15 ou 16 chiffres) :")
    if len(num) != 15 or len(num) != 16:
        while (False):
            try:
                input("Numero de carte bancaire (15 chiffres) :")
            except:
                pass

    savoir_carte(num)

def savoir_carte(num):
    premier = num[0]
    if premier == "3":
        print("AMEX")
    elif premier == "5":
        print("MASTERCARD")
    elif premier == "1":
        print("VISA")
    else:
        print("INVALID")



#AMEX : premier numero : 3

#Mastercard : premier numero : 5

#visa : premier numero : 1

main()
