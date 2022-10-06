from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as A
from lxml import html
from time import sleep
import csv
import openpyxl
import pandas as pd
import threading

df=pd.DataFrame(columns=[
        "Title",
        "Price",
        "Offre",
        "Nb_piece_vendu",
        "Etoile",
        "Envoi",
        "Boutique"
])

list_thread=[]




num=0
f=open("test.csv","a",newline="")
tup1=("Titre","price","Offre","Nb_piece_vendu","Etoile","Envoi","Boutique")
writer=csv.writer(f)
writer.writerow(tup1)
# driver=webdriver.Chrome('chromedriver')
#
prod=input("entez un produit:")
# driver.maximize_window()
# for page in range(1,2):
op = webdriver.ChromeOptions()
op.add_argument('headless')



def scrap(page):
    list_product=[]
    driver = webdriver.Chrome('chromedriver',options=op)

    # prod = input("entez un produit:")
    driver.maximize_window()
    num=0
    driver.get(f'https://fr.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={prod}&ltype=wholesale&SortType=default&page={page}')
    sleep(1)

    for i in range(24):
        driver.execute_script('window.scrollBy(0,200)',"")
        sleep(1)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(1)

    content=html.fromstring(driver.page_source)


    # elem = driver.find_element(By.TAG_NAME, 'body')
    #
    # i = 0
    # while i < 9:
    #     elem.send_keys(Keys.PAGE_DOWN)
    #     sleep(1)
    #     i += 1
    # sleep(10)
    # for i in range(24):
    #     driver.execute_script('window.scrollBy(0,200)',"")
    #     sleep(3)
    # driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # sleep(1)




    for produit in content.xpath('//a[@class="_3t7zg _2f4Ho"]'):
        Price = []
        Titre=produit.xpath('.//h1[@class="_18_85"]/text()')
        Prix=produit.xpath('.//div[@class="mGXnE _37W_B"]/span[1]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[2]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[3]/text()')+produit.xpath('.//div[@class="mGXnE _37W_B"]/span[4]/text()')
        if len(Prix)==2:
            Prix=Prix[0]+Prix[1]
            Price.append(Prix)
        elif len(Prix)==4:
            Prix=Prix[0]+Prix[1]+Prix[2]+Prix[3]
            Price.append(Prix)
        else:
            pass
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
        # d ={
        #     "Title":[Titre],
        #     "Price":[Price],
        #     "Offre":[Offre],
        #     "Nb_piece_vendu":[Nb_piece_vendu],
        #     "Etoile":[Etoile],
        #     "Envoi":[Envoi],
        #     "Boutique":[Boutique]
        # }
        # x=x.append({"Title":[Titre],"Price":[Price],"Offre":[Offre],"Nb_piece_vendu":[Nb_piece_vendu],"Etoile":[Etoile],"Envoi":[Envoi],"Boutique":[Boutique]},ignore_index=True)
        tup=(Titre[0], Price[0], Offre[0], Nb_piece_vendu[0], Etoile[0], Envoi[0], Boutique[0])
        writer.writerow(tup)
        print(tup)
#    return list_product

# f.close()

# readfile=pd.read_csv("produit.csv")
#
# readfile.to_excel("produit.xlsx",index=None,header=True)





for n in range(1,7):
    t = threading.Thread(target=scrap, args=(n,))
    list_thread.append(t)
    t.start()

# wait for the threads to complete
for t in list_thread:
    t.join()

list_thread=[]
for n in range(7,13):
    t = threading.Thread(target=scrap, args=(n,))
    list_thread.append(t)
    t.start()

# wait for the threads to complete
for t in list_thread:
    t.join()

f.close()
        # df=df.append(x,ignore_index=True)
# df.to_csv('test.csv')
# for i in range(1,6):
#     list_thread.append(threading.Thread(target=scrap,args=(i,)))
#
# for j in range(len(list_thread)):
#     list_thread[j].start()