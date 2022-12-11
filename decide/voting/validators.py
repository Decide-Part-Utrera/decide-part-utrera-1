
import unicodedata

def lofensivo(value):

    lsofensiva = ["caca", "pedo", "pis", "pilila", "ceporro", "tonto", "imbecil", "estupido", "idiota"]


    if("¿" in value):
        value=value.replace("¿", "")
    if("?" in value):
        value=value.replace("?", "")
    if("." in value):
        value=value.replace(".", "")
    if("," in value):
        value=value.replace(",", "")
    if("(" in value):
        value=value.replace("(", "")
    if(")" in value):
        value=value.replace(")", "")


    value = value.lower()
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    value = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', value).translate(trans_tab))
    palabras = value.split()

    porcentaje= 20 / 100
    cont = 0
    res= False

    for palabra in palabras:
        if(palabra in lsofensiva):
            cont+=1
        
    if(cont/len(palabras)>porcentaje):
        res=True
    return res
