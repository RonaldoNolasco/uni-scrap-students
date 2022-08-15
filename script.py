import requests as r
from bs4 import BeautifulSoup
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('6_esp.json', 'r') as f:
    json = json.load(f)

def obtenerCodigoUNI(codigoUNI):
    cod = str(codigoUNI)
    arr = [2,1,2,3,4,5,6,7]
    suma = 0
    for i in range(len(cod)):
        suma += int(cod[i]) * arr[i]
    return (cod + chr(65 + suma % 11))

i=0
while i<10000:
    codigoesp=""
    nombreesp=""
    codigo=obtenerCodigoUNI(2020*10000 + i)
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
        for x in json:
            if(x['nombre']==cod): #Ambos son del mismo tipo
                codigoesp = x['codigo']
                break
        print(codigo + " " + codigoesp + " " + nombre)
        i+=1
    elif(nombre=="None" and i%500!=0):
        i=((i//500)+1)*500
    else:
        i+=1

#Usar esta pagina: https://www.online-utility.org/text/sort.jsp para invertirlo y luego se agrega
#a la otra lista