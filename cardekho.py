import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


def process_new(car_id):

    
    # The first section is the same as process_new().
    url = 'https://www.cardekho.com/used-cars+in+bangalore?ID=' + car_id
    response = get(url)
    page_html = BeautifulSoup(response.text,'html.parser')
    page_title = page_html.find('title').text
    try:
        main_left = page_html.find('div', attrs = {'id':'main_left'})
    except:
        None
    

    if(page_title != 'Buy Used Car & Used Vehicle & Used Cars Bangalore - Cardekho.com' and
    str(main_left.find('strong', text = 'Availability').find_parent('tr').find_all('td')[1].text.replace('\n','')) == 'Available'): 


    # Here we obtain the vehicle's availability status. 
    try:
        avail = str(main_left.find('strong', text = 'Availability').find_parent('tr').find_all('td')[1].text.replace('\n',''))
    except:
        avail = None
    
    # We initialise a date_sold variable prior to the following if statement.
    date_sold = 0
    
    if avail == 'SOLD':
        try:
            updated = main_left.find('div', id = 'usedcar_postdate').text
            updated = re.findall(r"(?<=Updated on: )\w+-\w+-\w+",updated)[0]
            updated = datetime.strptime(updated,'%d-%b-%Y').date()
            date_today = datetime.now().date()
            if updated < date_today:
                date_sold = updated
            else:
                date_sold = date_today
        except:
            date_sold = datetime.now().date()

        return([date_sold, int(car_id)])
    
    # Else if the vehicle is still available for sale, we will update all of its details.   
    elif avail == 'Available':



# 1. Make and Model - e.g. Toyota Vios
        make_model = page_html.find('a', class_ = 'link_redbanner').text

        # 2. Price
        try:
            price = int(main_left.find('strong', text = 'Price').find_parent('tr').find_all('strong')[1].text.replace('$','').replace(',',''))
        except:
            price = 0

        # 3. Vehicle Type - e.g. 'Sports Car', 'Luxury Sedan'. Each car can only have one vehicle type.
        try:
            veh_type = main_left.find('strong', text = 'Type of Veh').find_parent('tr').find_all('td')[1].text
        except:
            veh_type = ''



        return([int(car_id), avail, make_model, price, veh_type])
    else:
        return None
