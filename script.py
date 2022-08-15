import requests as r
from bs4 import BeautifulSoup
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import datetime

import os

def loadSpeciality(inputPath):
    with open(inputPath, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def obtenerCodigoUNI(codigoUNI):
    cod = str(codigoUNI)
    arr = [2,1,2,3,4,5,6,7]
    suma = 0
    for i in range(len(cod)):
        suma += int(cod[i]) * arr[i]
    return (cod + chr(65 + suma % 11))

def main():
    speciality = loadSpeciality('speciality.json')

    fileName = "output/" + datetime.datetime.now().strftime("%Y-%d-%m %H%M%S") + ".csv"

    with open (fileName, mode='w') as file:
        i=0
        while i<10000:
            codigoesp=""
            nombreesp=""
            codigo=obtenerCodigoUNI(2022*10000 + i)
            url = "https://www.orce.uni.edu.pe/detaalu.php?id="+codigo+"&op=detalu"
            response = r.get(url, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            nombrerow = soup.tbody.find_all('tr')[5]
            codrow = soup.tbody.find_all('tr')[9] # bs4.element.Tag
            nombrecol = nombrerow.find_all('td')
            codcol = codrow.find_all('td') # bs4.element.ResultSet
            nombre = str(nombrecol[1].string)
            cod = str(codcol[1].string) #bs4.element.String to str
            if(nombre!="None"):
                for x in speciality:
                    if(x['nombre']==cod): #Ambos son del mismo tipo
                        codigoesp = x['codigo']
                        break
                joinRow = "|".join([codigo, codigoesp, nombre])
                file.write(joinRow + "\n")
                print(joinRow)
                i+=1
            elif(nombre=="None" and i%500!=0):
                i=((i//500)+1)*500
            else:
                i+=1

#Usar esta pagina: https://www.online-utility.org/text/sort.jsp para invertirlo y luego se agrega
#a la otra lista

if __name__ == "__main__":
    main()
