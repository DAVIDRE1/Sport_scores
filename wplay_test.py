from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import datetime as dt

website = "https://apuestas.wplay.co/es/PrimeraAColombia"
# Create a WebDriver instance for Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
# Visit the website
driver.get(website)

fecha = driver.find_element(By.XPATH, '''//div[@class = 'pager-item']''')

df = pd.DataFrame(columns=['datetime', 'local', 'cuota_local', 'cuota_empate', 'cuota_visitante', 'visitante', 'fecha', 'hora'])
quantity = len(fecha.find_elements(By.XPATH, './div'))

for i in range(1,quantity+1):
    l = [dt.datetime.now()]
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[4]/table/tbody/tr/td[1]/div/button/span/span[2]/span/span').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[4]/table/tbody/tr/td[1]/div/button/span/span[4]').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[4]/table/tbody/tr/td[2]/div/button/span/span[3]').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[4]/table/tbody/tr/td[3]/div/button/span/span[4]').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[4]/table/tbody/tr/td[3]/div/button/span/span[2]/span/span').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[2]/a/div[1]/span[2]').text)
    l.append(fecha.find_element(By.XPATH, f'//div[{i}]/div[2]/a/div[1]/span[1]').text)
    df.loc[len(df)] = l

driver.quit()
df.to_csv("../Users/davidramirez/Documents/MSDS/Personal_projects/Soccer/cuotas_wplay.csv", mode='a', index=False, header=False)