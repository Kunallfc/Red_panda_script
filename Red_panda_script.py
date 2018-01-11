from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import sqlite3

class red_panda_script:    
    def __init__(self):
        self.titlename    = ''
        self.rating       = ''                  
        self.google_search_textbox = 'lst-ib'
        self.movie_name = 'titleColumn'
        self.ratings    ='imdbRating'
        self.data_list  = []
    def browser_search(self):
        path=('/home/kunal/Desktop/chromedriver')
        driver = webdriver.Chrome(path)    
        driver.get('https://www.google.co.in')
        element = driver.find_element_by_id(self.google_search_textbox)
        element.send_keys('Top 250 imdb')
        element.submit()
        element = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/h3/a')
        element.click()
        self.titlename = driver.find_elements_by_class_name(self.movie_name)
        self.rating = driver.find_elements_by_class_name(self.ratings)        
        for i,j in zip(self.titlename,self.rating):
            info = dict()
            info['Name']     = i.text.encode('utf-8')
            info['Ratings']  = j.text.encode('utf-8')
            self.data_list.append(info)                
    def data_return(self):
        return (self.data_list)
    def save_data(self):
        db = sqlite3.connect('savedata.db')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IMDBLIST (NAME TEXT,RATINGS INTEGER)''')
        db.commit()
        for i,j in zip(self.titlename,self.rating):
            name= i.text
            ratings= j.text
            cursor.execute('''INSERT INTO IMDBLIST(NAME,RATINGS)VALUES(?,?)''',(name,ratings))
        db.commit()            
    def view_name(self):
        db = sqlite3.connect('savedata.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * from IMDBLIST''')
        all_rows = cursor.fetchall()
        for row in all_rows:
            print (row)



A=red_panda_script()
A.browser_search()
A.save_data()
A.view_name()
