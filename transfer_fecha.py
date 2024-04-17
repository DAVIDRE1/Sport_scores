from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import numpy as np
import json


def scrap_page(url, partidos, year, torneo, fase, jornada):
    # Create a WebDriver instance for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    # Visit the website
    driver.get(url)
    div_element = driver.find_element(By.CSS_SELECTOR, 'div.large-8.columns')
    boxes = div_element.find_elements(By.XPATH, 'div[@class="box"] [@style="border-top: 0 !important;"]')
    for i in range(len(boxes)):
        l = [year, torneo, fase, jornada]
        l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[1]/a''').get_attribute("innerText")) # home
        l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[5]/span/a/span''').get_attribute("innerText").split(":")[0]) # goals home
        l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[5]/span/a/span''').get_attribute("innerText").split(":")[1]) # goals visitor
        l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[8]/a''').get_attribute("innerText")) # visitor
        l.append(datetime.strptime(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[2]/td/a''').get_attribute("href").split("/")[-1], "%Y-%m-%d").date()) # date
        l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[2]/td''').get_attribute("innerText").split(",")[0]) # day
        try:
            l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[3]/td''').get_attribute("innerText").split("·")[-1].strip()) # referee
        except NoSuchElementException:
            l.append(np.nan) 
        try:
            l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[1]/span''').get_attribute("innerText").replace("(","").replace(".)","")) # pos home
        except NoSuchElementException:
            l.append(np.nan) 
        try:
            l.append(boxes[i].find_element(By.XPATH, f'''./table/tbody/tr[1]/td[8]/span''').get_attribute("innerText").replace("(","").replace(".)","")) # pos visitor
        except NoSuchElementException:
            l.append(np.nan)     

        if ((l[5] == "-") or (l[6] == "-")):
            l=l+[np.nan,np.nan,np.nan]
        elif l[5] > l[6]:
            l=l+[True,False,False]
        elif l[5] == l[6]:
            l=l+[False,True,False]
        else:
            l=l+[False,False,True]
        partidos.loc[len(partidos)] = l
    driver.quit()
    return partidos

def main():
    # load properties from configuration file
    try:
        with open("config_file.conf") as config:
            conf = json.load(config)
    except FileNotFoundError as e:
        print("Error: The file 'config_file.conf' was not found.")
        raise e
    partidos = pd.DataFrame(columns=['year', 'torneo', 'fase', 'jornada', 'local', 'goles_local', 'goles_visitante', 'visitante', 'fecha', 'dia', 'arbitro', 'pos_local', 'pos_visitante', 'gana_local', 'empate', 'gana_visitante'])
    website = f"https://www.transfermarkt.es/liga-dimayor-apertura/spieltag/wettbewerb/COLP/spieltag/{str(int(conf['fecha']))}/saison_id/{str(int(conf['year'])-1)}"
    partidos = scrap_page(website, partidos, int(conf['year']), conf["torneo"], conf["fase"], int(conf['fecha']))
    partidos["goles_local"] = partidos["goles_local"].replace("-",np.nan).astype(float)
    partidos["goles_visitante"] = partidos["goles_visitante"].replace("-",np.nan).astype(float)
    partidos.to_csv(conf["next_scores_file"], index=False, header=True)
    
if __name__ == "__main__":
    # the program execution starts here with the main method
    main()
