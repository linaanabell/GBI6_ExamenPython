# LINA ITURRALDE:

# Lista de librerías para el examen 
from Bio import Entrez
import re
import csv
import pandas as pd
import itertools

def download_pubmed(keyword): 
    """Con la función ENTREZ me permite hacer directamente la busqueda en la base
       datos de PUBMED y con las keyword que se emplearán en los ejercicios 
       dengue - cancer
    """
    Entrez.email = "gualapuro.moises@gmail.com"
    handle = Entrez.esearch (db = "pubmed",
                             term = keyword,
                             usehistory = "y")
    record = Entrez.read (handle)
    id_list = record ["IdList"]
    webenv = record["WebEnv"]
    query_key = record["QueryKey"]
    handle = Entrez.efetch(db="pubmed", 
                           rettype="medline", 
                           retmode="text", 
                           retstart=0, 
                           retmax = 1500, 
                           webenv = webenv, 
                           query_key = query_key)
    data = handle.read()
    data_2= re.sub(r'\n\s{6}', ' ', data)
    return (data_2)
    



def science_plots(data_2):
    """
    Mediante esta función vamos a buscar los países y los autores de la base de datos PubMed, con el fin de que contabilice el 
    número de autores por país y los que se obtienen con mayor repetición, ya que la variable país sera pa, es asi como mediante
    expresiones regulares se delimitará y se obtendrá las repeticiones de los autores
    """
    AD = []
    pa1 = []
    pa2 = []
    pa3 = []
    pa4 = []
    pa5 = []
    pa6 = []
    pa7 = []
    pa8 = []
    pa9 = []
    pa10 = []
    pa_T = []
    
    
    for line in data_2.splitlines():
        if line.startswith("AD  -"):
            AD.append(line[:])
    for line in data_2.splitlines():
        if line.startswith("AD  -"):
            AD = line[:]
            p1 = re.findall(r'\,\s(\w{2,16})\.', AD)
            pa1.append(p1)
            
            p2 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\.', AD)
            pa2.append(p2)
            
            p3 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\.', AD)
            pa3.append(p3)

            p4 = re.findall(r'\,\s(\w{2,16})\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            pa4.append(p4)

            p5 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            pa5.append(p5)

            p6 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            pa6.append(p6)
 
            p7 = re.findall(r'\,\s(\w{2,16})\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            pa7.append(p7)

            p8 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            pa8.append(p8)

            p9 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            pa9.append(p9)

            p10 = re.findall(r'\,\s\w{3,9}[0-9\-]\,\s(\w{2,16})\.', AD)
            pa10.append(p10)

            pa_T=pa1+pa2+pa3+pa4+pa5+pa6+pa7+pa8+pa9+pa10

    pa_T= list(itertools.chain.from_iterable(pa_T))
    len(pa_T)

    unique_pa_T = list(set(pa_T))
    unique_pa_T.sort()
    len(unique_pa_T)

    import csv
    
    coordenadas = {}
    with open('data/ubipais.txt') as f:
        csvr = csv.DictReader(f)
        for row in csvr:
            coordenadas[row['Name']] = [row['Latitude'], row['Longitude']]
    country = []
    longitude = []
    latitude = []
    almacen = []
    for z in unique_pa_T:
        if z in coordenadas.keys():
            country.append(z)
            latitude.append(float(coordenadas[z][0]))
            longitude.append(float(coordenadas[z][1]))
            almacen.append(pa_T.count(z))
    df_pa_T = pd.DataFrame()
    df_pa_T["Pais"] = country 
    df_pa_T["Numero de autores"] = almacen
   
    return (df_pa_T)