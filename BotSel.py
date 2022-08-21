from selenium import webdriver
from lxml import html
from time import sleep
import csv

num=0
f=open("produit.csv","a",newline="")
tup1=("Numero","Titre","price","Offre","Nb_piece_vendu","Etoile","Envoi","Boutique")
writer=csv.writer(f)
writer.writerow(tup1)
driver=webdriver.Chrome('chromedriver')

prod=input("entez un produit:")

for page in range(1,10):
    driver.get(f'https://fr.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={prod}&ltype=wholesale&SortType=default&page={page}')
    sleep(2)

    content=html.fromstring(driver.page_source)

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(2)


    for produit in content.xpath('//a[@class="_3t7zg _2f4Ho"]'):
        Price = []
        Titre=produit.xpath('.//h1[@class="_18_85"]/text()')
        Prix=produit.xpath('.//div[@class="mGXnE _37W_B"]/span[1]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[2]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[3]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[4]/text()')
        if len(Prix)==2:
            Prix=Prix[0]+Prix[1]
            Price.append(Prix)
        else:
            Prix=Prix[0]+Prix[1]+Prix[2]+Prix[3]
            Price.append(Prix)
        Offre=produit.xpath('.//div[@class="g_XRl"]/span[1]/text()')
        if (len(Offre)==0):
            Offre=['aucune offre']

        Nb_piece_vendu=produit.xpath('.//span[@class="_1kNf9"]/text()')
        if (len(Nb_piece_vendu)==0):Nb_piece_vendu=["NONE"]
        Etoile=produit.xpath('.//span[@class="eXPaM"]/text()')
        if len(Etoile)==0:
            Etoile=['pas d\'etoile']

        Envoi=produit.xpath('.//span[@class="_2jcMA"]/text()')
        if (len(Envoi)==0):Envoi=['NONE']
        Boutique=produit.xpath('.//a[@class="ox0KZ"]/text()')
        if (len(Boutique)==0):Boutique=['UNKNOWN']

        num+=1
        tup = (num,Titre[0], Price[0], Offre[0], Nb_piece_vendu[0], Etoile[0], Envoi[0], Boutique[0])
        writer.writerow(tup)
        print(tup)

f.close()