from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import csv
import re

driver = webdriver.Chrome()
driver.implicitly_wait(30)

###opens csv file and writes headers

csv_file = open('norwegian_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date', 'Departure time', 'Next departure time', 'Departure airport', 'Next departure airport', 'Arrival time', 'Next arrival time', 'Arrival airport', 'Next arrival airport', 'Best price, €', 'Taxes, €'])

###creates pages list

pages = []

for i in range(1, 29):
    url = 'https://www.norwegian.com/en/ipc/availability/avaday?D_City=OSLALL&A_City=RIX&TripType=1&D_Day=0' + str(i) + '&D_Month=201905&D_SelectedDay=01&R_Day=31&R_Month=201905&R_SelectedDay=31&IncludeTransit=false&AgreementCodeFK=-1&CurrencyCode=EUR&mode=ab'
    pages.append(url)

###finds all the data and writes it to a csv file (also prints in the terminal)
    
for item in pages:
    driver.get(item)
    source3 = driver.execute_script("return document.documentElement.outerHTML")
    soup3 = BeautifulSoup(source3, 'lxml')

    try:
        for info in soup3.find_all('table', class_='avadaytable'):
            date = driver.find_element_by_xpath('//*[@id="avaday-outbound-result"]/div/div/div[1]/table/tbody/tr/td[2]')
            date = date.text.strip()
            print(date)
            
            row_first = info.find('tr', class_='oddrow rowinfo1')
            departure_time = row_first.find('td', class_='depdest').text
            print('Departure time: ' + departure_time)

            try:
                row_first2 = info.find('tr', class_='evenrow rowinfo1')
                departure_time2 = row_first2.find('td', class_='depdest').text
                print('Departure time: ' + departure_time2)
            except:
                departure_time2 = None
                print(departure_time2)

            arrival_time = row_first.find('td', class_='arrdest').text
            print('Arrival time: ' + arrival_time)

            try:
                arrival_time2 = row_first2.find('td', class_='arrdest').text
                print('Arrival time: ' + arrival_time2)
            except:
                arrival_time2 = None
                print(arrival_time2)
            
            try:
                cheapest_price = row_first.find('td', class_='fareselect standardlowfare').text
                print('Cheapest price: ' + cheapest_price)
            except AttributeError:
                try:
                    cheapest_price = row_first.find('td', class_='fareselect standardlowfareplus').text
                    print('Cheapest price: ' + cheapest_price)
                    driver.find_element_by_xpath('//*[@id="FlightSelectOutboundStandardLowFarePlus0"]').click()
                    tax = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_ipcAvaDay_upnlResSelection"]/div[1]/div/table/tbody/tr[20]/td[2]')
                    tax = tax.text.replace("€", "")
                    print('Taxes: ' + tax)
                except AttributeError:
                    cheapest_price = row_first.find('td', class_='fareselect standardflex endcell').text
                    print('Cheapest price: ' + cheapest_price)
                    driver.find_element_by_xpath('//*[@id="FlightSelectOutboundStandardFlex0"]').click()
                    tax = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_ipcAvaDay_upnlResSelection"]/div[1]/div/table/tbody/tr[18]/td[2]')
                    tax = tax.text.replace("€", "")
                    print('Taxes: ' + tax)

            try:
                cheapest_price2 = row_first2.find('td', class_='fareselect standardlowfare').text
                print('Cheapest price: ' + cheapest_price2)
            except:
                cheapest_price2 = None
                print(cheapest_price2)
            
            row_second = info.find('tr', class_='oddrow rowinfo2')
            departure_airport = row_second.find('td', class_='depdest').text
            print('Departure airport: ' + departure_airport)

            try:
                row_second2 = info.find('tr', class_='evenrow rowinfo2')
                departure_airport2 = row_second2.find('td', class_='depdest').text
                print('Departure airport: ' + departure_airport2)
            except:
                departure_airport2 = None
                print(departure_airport2)
            
            arrival_airport = row_second.find('td', class_='arrdest').text
            print('Arrival airport: ' + arrival_airport)

            try:
                arrival_airport2 = row_second2.find('td', class_='arrdest').text
                print('Arrival airport: ' + arrival_airport2)
            except:
                arrival_airport2 = None
                print(arrival_airport2)

            try:
                driver.find_element_by_xpath('//*[@id="FlightSelectOutboundStandardLowFare0"]').click()
                tax = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_ipcAvaDay_upnlResSelection"]/div[1]/div/table/tbody/tr[18]/td[2]')
                tax = tax.text.replace("€", "")
                print('Taxes: ' + tax)
            except:
                pass

            csv_writer.writerow([date, departure_time, departure_time2, departure_airport, departure_airport2, arrival_time, arrival_time2, arrival_airport, arrival_airport2, cheapest_price, tax])    
    except:
        print('Error. Something went wrong.')

###closes csv file and browser window
        
csv_file.close()
driver.quit()
