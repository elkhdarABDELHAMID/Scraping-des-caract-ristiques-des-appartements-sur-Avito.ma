from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)






def ChargeLien_Page(nombre):
    link_tout_page = []
    link_principal = "https://www.avito.ma/fr/maroc/appartements"
    driver.get(link_principal)

    for i in range(1, nombre + 1):
        demi_link = f"{link_principal}?o={i}"
        driver.get(demi_link)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='sc-1lz4h6h-0 bsvCex']"))
            )
            link_tout_page.append(driver.current_url)
            print(f"Le lien de la page {i} est ajouté : {link_tout_page[-1]}")
            time.sleep(3)
        except Exception as e:
            print(f"Erreur de chargement de la page {i} : {e}")
            break

    return link_tout_page


def lienChauqueAppartement(link_tout_page):
    chaque_annonce = set()
    xpath_annonces = "//div[@class='sc-1lz4h6h-0 bsvCex']//a"

    for lien in link_tout_page:
        driver.get(lien)
        try:
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, xpath_annonces))
            )
            annonces = driver.find_elements(By.XPATH, xpath_annonces)
            for annonce in annonces:
                lien_chaque_annonce = annonce.get_attribute("href")
                chaque_annonce.add(lien_chaque_annonce)
                print(f"Lien de l'appartement : {lien_chaque_annonce}")
        except Exception as e:
            print(f"Erreur lors de l'extraction des liens : {e}")

    return list(chaque_annonce)

def detai_appartement(chaque_annonce):
    information_appartement = []

    with open("information_appartement.csv", mode="w", newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(['Title','Price','Location','Surface','Rooms','Bathrooms','Floor','Construction Year'])

        for chaque in chaque_annonce:
            driver.get(chaque)
            time.sleep(3)

            try:
                Title = fun_xpath("//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/h1")
                Location = fun_xpath("//*[@id='__next']/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]")
                Price = fun_xpath('//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p')

                Surface = fun_xpath("//li[.//span[text()='Surface habitable']]/span[@class='sc-1x0vz2r-0 gSLYtF']")
                Floor = fun_xpath("//li[.//span[text()='Étage']]/span[@class='sc-1x0vz2r-0 gSLYtF']")
                Rooms = fun_xpath('//[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[1]/div/span')
                Bathrooms = fun_xpath('//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div/span')
                Construction_Year = fun_xpath("//li[.//span[text()='Âge du bien']]/span[@class='sc-1x0vz2r-0 gSLYtF']")
                
                write.writerow([Title, Location,Price ,Surface, Floor, Floor, Rooms,Bathrooms, Construction_Year])
            except Exception as e:
                print(f"Erreur lors de  details de l'annonce : {e}")

def fun_xpath(xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except Exception:
        return "N/A"

# Pour executer les fonctions en test
try:
    pages = ChargeLien_Page(3)
    annonces = lienChauqueAppartement(pages)
    detai_appartement(annonces)
finally:
    driver.quit()



