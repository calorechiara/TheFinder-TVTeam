# Import the libraries
import numpy as np
from utils.feature_extractor import FeatureExtractor 
from PIL import Image
import os
import re

#Funzione utilizzata per ordinare i nomi delle immagini presenti nel vettore data (image_names)
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def compara(input):
    fe=FeatureExtractor()
    features=[]
    image_names = sorted_alphanumeric(os.listdir("gallery/"))

    #recupero le feature dai file e le appendo a una lista
    for filename in image_names:
        nomeFile = os.path.splitext(filename)[0]
        features.append(np.load(f"features/{nomeFile}.npy"))

    features=np.array(features)                                 #rendo la lista un Numpy Array   
    img = Image.open("images/"+input)                           #carico l'immagine di query
    query = fe.extract(img)                                     #estraggo le features con il metodo extract della classe esterna FeatureExtractor
    
    #calcolo la distanza euclidea fra la feature della query e quelle recuperate dal dataset
    dists = np.linalg.norm(features - query, axis=1)            #np.linalg.norm formula per distanza eucl
    ids = np.argsort(dists)                                     #argsort è funzione che ordina in ordine crescente e ritorna gli indici(corrispondenti all'id dell'immagine)

    #creo nuovo array per definire punteggio da 0 a 100
    #-------------------------------------------------------------------
    arr2=np.sort(dists)                    #in arr2 ho i valori ordinati in ordine crescente
    
    oldMax=arr2[len(arr2)-1]              #il vecchio massimo è l'ultimo elemento dell'arr2(che era stato ordinato)    
    if(arr2[0]>0.5):                      #se sono particolarmente simili la distanza sarà a grandi linee inferiore di 0,5
        oldMin=0.5                        #per aumentare i punteggi lavorare su questo(aumentarlo)
    else:
        oldMin=arr2[0]                    #per non avere percentuali che superino il 100% se la distanza minima è minore di 0.5
    newMax=100                            #nuovo punteggio massimo
    newMin=0                              #nuovo minimo

    OldRange = (oldMax-oldMin)            #vecchio range
    NewRange = (newMax-newMin)            #nuovo range
    new=[]
    for n in dists:
        new.append(100-(((n - oldMin) * NewRange) / OldRange) + newMin) #formula per passare da vecchio range a nuovo range(100- per invertire l'ordine 
                                                                        #(sennò avrei che i più simili sono quelli più vicini allo 0)                                                                  
    #--------------------------------------------------------------------

    result = []
    #Creazione array (ordine decrescente) contente associazione tra nomi file(senza formato) e percentuali: [(654,97.8),(231,94.2),....]
    for i in ids:
        nomeFile = os.path.splitext(image_names[i])[0]
        result.append((nomeFile, new[i]))
    return result
