import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import csv 
import time 
import urllib.request
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os 
os.chdir("/Users/susanchen/Documents/GitHub/skincare_classification")


def get_links(pageLinksList):
    # extract links of all products listed on the page
    Links = []
    for page in pageLinksList:
        prod_pg = requests.get(page)
        soup = BeautifulSoup(prod_pg.text, 'html.parser')
        block = soup.find_all("div", class_= 'prod-title-desc')
        
        for link in block:
            l= link.find('p').a.get('href')
            Links.append('https://ulta.com'+l)

    return Links

def scrape(linkArray):
    for link in linkArray:
        try:

            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=1.0)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            productPage = session.get(link, verify = False)

            #productPage = requests.get(link, verify = False)
            Soup = BeautifulSoup(productPage.text, 'html.parser')

            # extract product name 
            name = Soup.find('div', class_ = 'ProductMainSection__productName').text
            product_name.append(name)

            # extract brand name 
            b = Soup.find('div', class_ = "ProductMainSection__brandName").text
            brand.append(b)

            # extract product price 
            p = Soup.find('div', class_ = 'ProductPricingPanel').text.strip()
            price.append(p[6:])

            # extract product ingredients
            try: 
                i = Soup.find('div',  class_ = 'ProductDetail__ingredients').text.strip()
                ingredients.append(i[11:])
            except AttributeError:
                ingredients.append('')

            # extract product rating 
            #try:
                #rating = Soup.find("div", class_='pr-snippet').text.strip()
                #ratings.append(rating)
            #except AttributeError:
                #ratings.append("")

            # extract product recommendation % 
            #try:
                #recommendation = Soup.find("div", class_='pr-reco.pr-reco-green').text.strip()
                #recommendations.append(recommendation)
            #except AttributeError:
                #recommendations.append("")

        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue




    #get_num_reviews()
    #get_rating()
    #unable to extract rating and review

    data = {"Product": product_name, 'Brand': brand, "Ingredients": ingredients, 'Price': price}
    return data

#def preclean(dataframe):
    ### needs to be complete
    ## remove $ from price column
    ## remove ingredients from ingredients column 
    #for i in range(len(dataframe)):

def save(data, fileName):
    df = pd.DataFrame(data)
    #preclean(df)
    df.to_csv(fileName + ".csv", index = False)


if __name__ == "__main__":

    ## Oily Collection 
    listOfOilyPages = ["https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=0&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=192&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=288&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=384&Nrpp=96" , "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3j", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3j&No=96&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3j&No=192&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3j&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3j&No=384&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=0&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=96&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=192&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=288&Nrpp=96","https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=384&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3j&No=480&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3j&No=0&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3j&No=96&Nrpp=96", "https://www.ulta.com/skin-care-suncare?N=27feZ1z13p3j", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3j&No=96&Nrpp=96", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3j&No=96&Nrpp=96"]
    product_name = []
    brand =[]
    price = []
    ingredients = []
    ratings = []
    recommendations = []
    oily_links = get_links(listOfOilyPages)
    oily_data = scrape(oily_links)
    save(oily_data, 'Oily')
    

    ## Normal Collection 
    listOfNormPages = ["https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3l&No=0&Nrpp=96","https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3l&No=96&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3l&No=192&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3l&No=288&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3l&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=0&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=96&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=192&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3l&No=480&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=0&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=96&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=192&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=288&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=384&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=480&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3l&No=576&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3l&No=0&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3l&No=96&Nrpp=96", "https://www.ulta.com/skin-care-suncare?N=27feZ1z13p3l", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3l&No=0&Nrpp=96", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3l&No=96&Nrpp=96"]
    product_name = []
    brand =[]
    price = []
    ingredients = []
    ratings = []
    recommendations = []
    norm_links = get_links(listOfNormPages)
    norm_data = scrape(norm_links)
    save(norm_data, 'Normal')

    ## Dry Collection 
    listOfDryPages = ["https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3o&No=0&Nrpp=96","https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3o&No=96&Nrpp=96","https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3o&No=192&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3o&No=288&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3o&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=0&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=96&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=192&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3o&No=480&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=0&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=96&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=192&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=288&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=384&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3o&No=480&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3o&No=0&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3o&No=96&Nrpp=96", "https://www.ulta.com/skin-care-suncare?N=27feZ1z13p3o", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3o&No=0&Nrpp=96", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3o&No=96&Nrpp=96"]
    product_name = []
    brand =[]
    price = []
    ingredients = []
    ratings = []
    recommendations = []
    dry_links = get_links(listOfDryPages)
    dry_data = scrape(dry_links)
    save(dry_data, 'Dry')

    ## Combination Collection 
    listOfComboPages = ["https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=0&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=192&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=288&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3k&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=0&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=192&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=384&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3k&No=480&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=0&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=192&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=288&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=384&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=480&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3k&No=576&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3k&No=0&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/skin-care-suncare?N=27feZ1z13p3k", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3k&No=96&Nrpp=96", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3k&No=0&Nrpp=96"]
    product_name = []
    brand =[]
    price = []
    ingredients = []
    ratings = []
    recommendations = []
    combo_links = get_links(listOfComboPages)
    combo_data = scrape(combo_links)
    save(combo_data, 'Combination')

    ## Sensitive Collection 
    listOfSenPages = ["https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3m&No=0&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3m&No=96&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3m&No=192&Nrpp=96", "https://www.ulta.com/skin-care-cleansers?N=2794Z1z13p3m&No=288&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3m&No=0&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3m&No=96&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3m&No=192&Nrpp=96", "https://www.ulta.com/skin-care-moisturizers?N=2796Z1z13p3m&No=288&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3m&No=0&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3m&No=96&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3m&No=192&Nrpp=96", "https://www.ulta.com/skin-care-treatment-serums?N=27csZ1z13p3m&No=288&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3m&No=0&Nrpp=96", "https://www.ulta.com/skin-care-eye-treatments?N=270kZ1z13p3m&No=96&Nrpp=96", "https://www.ulta.com/skin-care-suncare?N=27feZ1z13p3m","https://www.ulta.com/korean-skin-care?N=27igZ1z13p3m&No=0&Nrpp=96", "https://www.ulta.com/korean-skin-care?N=27igZ1z13p3m&No=96&Nrpp=96"]
    product_name = []
    brand =[]
    price = []
    ingredients = []
    ratings = []
    recommendations = []
    sen_links = get_links(listOfSenPages)
    sen_data = scrape(sen_links)
    save(sen_data, 'Sensitive')


