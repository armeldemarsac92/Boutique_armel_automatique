import json

with open ("../Assets/Catalogs/size_catalog.json", "r") as data:
    dictionnaire=json.load(data)
input = input("votre taille?")

def return_value(input):
    taille = dictionnaire[input]
    print(taille)


return_value(input)

