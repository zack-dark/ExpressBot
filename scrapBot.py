import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pd

df=pd.DataFrame(columns=[
        "Title",
        "Price",
        "Qty_sold",
        "Ranting",
        "Shipping",
        "Store"
])

session=HTMLSession()
headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


url="https://fr.aliexpress.com/?gatewayAdapt=glo2fra"

result=session.get("https://fr.aliexpress.com/?gatewayAdapt=glo2fra")

result.html.render(sleep=2,timeout=20)
categories= result.html.find("#home-firstscreen > div > div > div.categories-main > div > div > div.categories-list-box > dl.cl-item")

# print(categories.text)
# print(list(categories.absolute_links)[0])

categorie_list=[]
for cats in categories:
    categorie_link=list(cats.absolute_links)[0]
    categorie_name=cats.text
    categorie_dict={
        "name":categorie_name,
        "link":categorie_link
    }
    categorie_list.append(categorie_dict)

#print(categorie_list)
result=session.get(categorie_list[0]["link"])
result.html.render(sleep=4,timeout=20,scrolldown=14)
products=result.html.find("#root > div.glosearch-wrap > div > div.main-content > div.right-menu > div > div.JIIxO > a._3t7zg")

#print(len(products))
for product in products:
    try:
        product_title=product.find("._18_85",first=True).text
        product_price= product.find(".mGXnE", first=True).text
        quantity_sold=product.find("._1kNf9",first=True).text
        ranting=product.find(".eXPaM",first=True).text
        shipping=product.find("._2jcMA",first=True).text
        store=product.find(".ox0KZ",first=True).text
        dfnew = pd.DataFrame({
            "Title": [product_title],
            "Price": [product_price],
            "Qty_sold": [quantity_sold],
            "Ranting": [ranting],
            "Shipping": [shipping],
            "Store": [store]
        })
        df=pd.concat([df,dfnew])
    except AttributeError:
        pass



df.to_csv("aliexpress.csv")
print(df)




























#
#
# src=result.content
# #print(src)
#
#
# soup=BeautifulSoup(src,'lxml')
# #print(soup)
#
#
# link_tag=soup.find_all("div",{"id":"root"})
# print(link_tag)
# # links_url=[]
# # for i in link_tag:
# #     links_url.append(i.get('href'))
# #     #print(i.get('href'))
# #
# # #for i in range(len(links_url)):
# # result_links=requests.get(links_url[0])
# # src_links=result_links.content
# # soup_links=BeautifulSoup(src_links,'lxml')
# # titles=soup.find_all("a")
# #
# # print(links_url)
# #
# # print(titles)