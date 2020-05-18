from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    #table = soup.find(___) 
    table = soup.find('table', attrs={'class':'table'})
    #tr = table.find_all(___) 
    tr = table.find_all('tr')

    temp = [] #initiating a tuple
    
    import re
    listm = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember']
    listmn = ['1','2','3','4','5','6','7','8','9','10','11','12']


    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        #use the key to take information here
        #name_of_object = row.find_all(...)[0].text

        #get exchange date
        ExchangeDate = row.find_all('td')[0].text.replace('\xa0','-')
        ExchangeDate = ExchangeDate.strip() #for removing the excess whitespace
        
        for i in range(len(listm)):  
            if re.search(listm[i],ExchangeDate):
               ExchangeDate = re.sub(listm[i],listmn[i],ExchangeDate)
               break
        
        #get exchange ask
        ask = row.find_all('td')[1].text.replace(',','.')
        ask = ask.strip() #for removing the excess whitespace
    
        #get exchange Bid
        bid = row.find_all('td')[2].text.replace(',','.')
        bid = bid.strip() #for removing the excess whitespace

        #temp.append((___)) #append the needed information 
        temp.append((ExchangeDate,ask,bid)) 
    
    temp = temp[::-1] #remove the header

    #df = pd.DataFrame(temp, columns = (___)) #creating the dataframe
    df = pd.DataFrame(temp, columns = ('tanggal','Kurs Jual','Kurs Beli'))
    
   #data wranggling -  try to change the data type to right data type
    df['Kurs Beli'] = df['Kurs Beli'].astype('float64')
    df['Kurs Jual'] = df['Kurs Jual'].astype('float64')

   #end of data wranggling

    return df

@app.route("/")
def index():
    #df = scrap(___) #insert url here
    df = scrap("https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019")

    #This part for rendering matplotlib
    #fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
