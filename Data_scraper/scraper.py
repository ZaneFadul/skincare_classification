import json
import pandas as pd
import numpy as np 
import csv
import time
import urllib.request
import requests
import sqlite3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class SkinTypeDatabase:
    def __init__(self, name, skintypes):
        self.conn = sqlite3.connect(f'{name}.db')
        self.c = self.conn.cursor()
        try:
            tables = ['skintypes', 'links', 'products', 'ingredients', 'pi_records']
            for table in tables:
                self.c.execute(f'DROP TABLE IF EXISTS {table}')
            
            #Create Skin ID Guided Vocabulary Table
            self.c.execute('''CREATE TABLE IF NOT EXISTS skintypes(
                           skin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           skintype TEXT NOT NULL
                           )''')
        
            #Create Links Table
            self.c.execute('''CREATE TABLE IF NOT EXISTS links(
                           link_id INTEGER PRIMARY KEY,
                           link TEXT NOT NULL,
                           skin_id INTEGER,
                           FOREIGN KEY(skin_id) REFERENCES skintypes(skin_id)
                           )''')
        
            #Create Product Table
            self.c.execute('''CREATE TABLE IF NOT EXISTS products(
                            product_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            brand TEXT NOT NULL,
                            price FLOAT,
                            rating INTEGER,
                            recommendation INTEGER
                           )''')
            
            #Create Ingredient Table
            self.c.execute('''CREATE TABLE IF NOT EXISTS ingredients(
                           ingredient_id INTEGER PRIMARY KEY,
                           name TEXT NOT NULL
                           )''')
            
            #Create Product Ingredient Records Table
            self.c.execute('''CREATE TABLE IF NOT EXISTS pi_records(
                             record_id INTEGER PRIMARY KEY,
                             product_id INTEGER NOT NULL,
                             ingredient_id INTEGER NOT NULL,
                             ingredient_weight FLOAT NOT NULL,
                             FOREIGN KEY(product_id) REFERENCES products(product_id),
                             FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
                             )''')
            
            #Insert Skintypes
            skintypes = [(i,) for i in skintypes]
            skintypes = str(tuple(skintypes)).replace('\'','\"').replace(',)',')')[1:-1]
            self.c.execute(f'INSERT INTO skintypes (skintype) VALUES {skintypes}')
            print(self.c.execute('SELECT * FROM skintypes').fetchall())
            self.conn.commit()
        except:
            pass
        
    def close(self):
        self.conn.commit()
        self.conn.close()
        
class SkinTypeScraper:
  def __init__(self, skintype):
    self.skintype = skintype
    self.names = []
    self.brands = []
    self.prices = []
    self.ingredients = []
    self.ratings = []
    self.recommendations = []
    self.links = []  #getLinks
    
    def get_links(self, pages, domain='https://ulta.com'):
        for page in self.pages:
            prod_pg = requests.get(page)
            soup = BeautifulSoup(prod_pg.text, 'html.parser')
            block = soup.find_al('div', class_='prod-title-desc')
            for link in block:
                l = link.find('p').a.get('href')
                self.links.append(f'{domain}{l}')
                
    def scrape(self):
        for link in self.links:
            try:
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=1.0)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                
                productPage = session.get(link, verify = False)
                
                Soup = BeautifulSoup(productPage.text, 'html.parser')
                
                #Extract Product Name
                name = Soup.find('div', class_ = 'ProductMainSection__productName').text
                self.names.append(name)
                
                #Extract Brand Name
                b = Soup.find('div', class_ = 'ProductMainSection__brandName').text
                self.brands.append(b)

                #Extract Product Ingredients
                try:
                    i = Soup.find('div', class_ = 'ProductDetail__ingredients').text.strip()
                    self.ingredients.append(i)
                except:
                    self.ingredients.append('')
                    
            except:
                print('Connection Refused... Resume in 3 seconds')
                time.sleep(3)
                continue
            
            return
    
if __name__ == '__main__':  
    skintype_names = [  
    'normal',
    'oily',
    'dry',
    'sensitive',
    'combination'
    ]

    skintypes = [ SkinTypeScraper(i) for i in skintype_names ]
    db = SkinTypeDatabase('database', skintype_names)
        
    #Commit and Close
    db.close()  