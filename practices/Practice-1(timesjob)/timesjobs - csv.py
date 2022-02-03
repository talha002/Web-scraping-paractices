from os import link
import re
from bs4 import BeautifulSoup
import requests
from requests.api import head, request
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv

#Veri toplanılacak siteye erişim için gerekli olan kodlamalar:

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=N&sequence=1&startPage=1")
time.sleep(10)
close_it = driver.find_element_by_id("closeSpanId").click()

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=', timeout=55).text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

#Web sayfasından istenilen verileri (varolan konseptte iş ilanları) toplamak için yazılmış olan fonksiyon:
def is_bul():

# İlk sayfadaki veriler toplandıktan sonra bir sonraki sayfaya geçmek için kullanılacak kdolamalar:
    html_text = requests.get(next_page).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

#Varolan iş ilanlarının kategorize edilmesi için yapılan işlemler:
    for job in jobs:

        company_name = job.find('h3', class_ = 'joblist-comp-name').text.strip()
        skills = job.find('span', class_ = 'srp-skills').text.strip()
        date = job.find('span', class_ = 'sim-posted').text.strip()

#Sadece yayınlama tarihi bir kaç gün olan iş ilnalarını alması için yazılan kod:
        if "few" in date:
                list_of_jobs = [company_name, skills, date]
                writer.writerow(list_of_jobs)
        else:
            continue

#Bir sonraki sayfaya geçmek için yazılmış olan kodlamalar:
page_nums = soup.find("div", class_ = "srp-pagination clearfix")
active_page_num = int(page_nums.find("em", class_ = "active").text)
#Daha önceden yapılmış olan katergorilerin türkçe başlıkları (csv dosyasında kullanılacaktır):
headers = ["Sirket ismi", "Gereklilikler", "Yayinlanma tarihi"]

#CSV dosyasını oluşturma ve editleme:
with open("deneme.csv", "w") as deneme:
    writer = csv.writer(deneme)
    writer.writerow(headers)

    while active_page_num < 5:
        active_page_num += 1

        #10. sayfadan sonra tıklanması gereken link_text'i "next 10 pages" olduğu için ve "if 1 in active_page_num" fonksiyonu bütün 10'lu sayıları eleyeceği için (örneği 12.sayfa, 13.sayfa...) burada "if" fonksiyonuna ve devamında gereken işlemlere ihtiyaç vardır.
        if active_page_num == 11:
            next_page_num = driver.find_element_by_link_text("Next 10 pages")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ActionChains(driver).move_to_element(next_page_num).click().perform()
            next_page = driver.current_url
            print(next_page)
            active_page_num += 1
            is_bul()
            time.sleep(2)
        #her son basamağı "1" ile biten sayıdan sonra (örneğin, 21, 31, 41...) tıklanması gereken link_text'i "next 10 pages" olduğu için burada "if active_page_num>19 and 1 in" fonksiyonuna ve devamında gereken işlemlere ihtiyaç vardır.
        elif active_page_num >19 and "1" in str(active_page_num):
            next_page_num = driver.find_element_by_link_text("Next 10 pages")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ActionChains(driver).move_to_element(next_page_num).click().perform()
            next_page = driver.current_url
            print(next_page)
            active_page_num += 1
            is_bul()
            time.sleep(2)
        #Yukarada tarif edilen sayılar dışındaki sayfaların (örneğin, 2, 3, 4, 5, 22, 23, 24, 25...) normal bir şekilde açılması için gereken fonksiyon else'tir
        else:
            next_page_num = driver.find_element_by_link_text(str(active_page_num))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ActionChains(driver).move_to_element(next_page_num).click().perform()
            next_page = driver.current_url
            print(next_page)
            is_bul()
            time.sleep(2)
    else:
        print("Son sayfaya ulaşıldı!")
#CSV dosyasının kapatılması:
deneme.close