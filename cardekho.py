from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import time
import random
headers = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

def get_basic_info(content_list):
    basic_info = []
    for item in content_list:
        basic_info.append(item.find_all('div', attrs={'class': 'car-ad-info'}))
    return basic_info

def get_names(basic_info):
    names = []
    for item in basic_info:
        for i in item:
            names.append(i.find_all("h2", attrs = {"class" : "car-ad-name"})[0].text.strip())
    return names

def get_years(basic_info):
    years = []
    for item in basic_info:
        for i in item:
            years.append(i.find_all("h3", attrs = {"class" : "car-ad-year"})[0].text.strip())
    return years

def get_prices(basic_info):
    prices = []
    for item in basic_info:
        for i in item:
            prices.append(i.find_all("div", attrs = {"class" : "car-ad-price"})[0].string.replace(u'\xa0', u' ').strip())
    return prices

def get_motor(basic_info):
    tables = []
    motors = []
    mileages = []
    data = [motors, mileages]
    for item in basic_info:
        for i in item:
            tables.append(i.find_all("table", attrs = {"class" : "used-specs-table"})[0])
    for table in tables:
        motors.append(table.find("td", attrs={"class" : "car-ad-cc"}).string)
        mileages.append(table.find("td", attrs={"class" : "car-ad-km"}).string)
    return data

page_number = 1
names = []
prices = []
years = []
motors = []
mileages = []


for i in range(9):
    base_url = "https://www.cardekho.com/newcars".format(page_number)
    response = get(base_url, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    content_list = html_soup.find_all('div', attrs={'class': 'car-ad sft-ad'})

    basic_info = get_basic_info(content_list)
    names1 = get_names(basic_info)
    prices1 = get_prices(basic_info)
    years1 = get_years(basic_info)
    motors1 = get_motor(basic_info)[0]
    mileages1 = get_motor(basic_info)[1]

    names.extend(names1)
    prices.extend(prices1)
    years.extend(years1)
    motors.extend(motors1)
    mileages.extend(mileages1)
    page_number = page_number + 1
    time.sleep(random.randint(1,2))

cols = ["Name", "Year", "Motor", "Mileage (Km)", "Price"]
data = pd.DataFrame({"Name" : names, "Year" : years, "Motor" : motors, "Mileage (Km)": mileages, "Price" : prices})[cols]
data["Price"] = data["Price"].replace({'\$ ':''}, regex = True)
data["Price"] = data["Price"].replace({'\,':''}, regex = True)
data["Mileage (Km)"] = data["Mileage (Km)"].replace({'\ Km':''}, regex = True)
data[["Mileage (Km)", "Year", "Motor", "Price"]] = data[["Mileage (Km)", "Year", "Motor", "Price"]].apply(pd.to_numeric)

data.head()
data.drop_duplicates().to_excel('Car_list.xls')
#Some filters
#data.loc[(data["Price"] < 50000000) & (data["Motor"] == 1200)].drop_duplicates()
