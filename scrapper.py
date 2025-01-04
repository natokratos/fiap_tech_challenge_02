import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import re
import platform 
import io

class Scrapper:

    def __init__(self):
        
        self.source_url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

    def download_data(self, url):
        '''
        Realizar a requisição HTTP e retornar o conteúdo
        '''

        try:
            if "Linux" in platform.system():
                service = Service(executable_path="./geckodriver-linux")
            elif "Windows" in platform.system():
                service = Service(executable_path="./geckodriver.exe")
            else:
                service = Service(executable_path="./geckodriver")

            options = Options()
            # options.headless = True
            options.add_argument("--headless")
            #options.add_argument(r"--binary_location C:\Users\darkt\Apps\FirefoxPortable\App\Firefox64")
            # options.add_argument('--binary_location /usr/bin/firefox')
            # options.binary_location=r"/usr/bin/firefox"
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(url) 
            elems = driver.find_elements(By.XPATH,  "//*[contains(@href, 'indexPage/')]")
            #all_href = driver.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            content = {}
            for elem in elems:
                #if elem.get_attribute('href') not in content and not elem.get_attribute('href').endswith("indexPage/"):
                if not elem.get_attribute('href').endswith("indexPage/"):
                    #print(elem.get_attribute('href'))
                    content[elem.text.replace(' ','_').replace('-','').replace('.','').replace('ª','')] = elem.get_attribute('href')
            #print(all_href)
            driver.quit()
            # response = requests.get()
            # response.raise_for_status()

            
            # if response.content:
            #     soup = BeautifulSoup(response.content, 'html.parser')
            #     btn_download = soup.find('app-root')
            #     print(f"btn_download {btn_download}")
            #     if btn_download and 'href' in btn_download.attrs:
            #         content = f"{self.source_url}/{btn_download['href']}"
            # print(f"\n\ncontent{response.content}")
            # print(f"\n\ncontent{response.json}")
            #print(list(content))
            return content
        except requests.RequestException as e:
            #file_name = url.split("=")[-1]
            file_name = url.split("/")[-1]
            print(f"options[file_name] {options[file_name]}")
            if options and not options[file_name]:
                file_name = f"{options[file_name]}_default.csv"
            elif sub_options and not sub_options[file_name]:
                file_name = f"{sub_options[file_name]}.csv"
            print(f"file_name {file_name}")
            pattern = re.compile(f"{file_name}[^ ]+.csv")
            found = False
            #print(f"pattern {pattern}")
            for fp in os.listdir("src/database/temp_files/"):
                match = pattern.match(fp)
                #print(f"fp {fp} match {match}")
                if match:
                    file_name = f"src/database/temp_files/{str(match.group(0))}"
                    print(f"O CSV correspondente [{file_name}] existe, tamanho [{os.path.getsize(file_name)}]")
                    #response = BeautifulSoup(open(file_name, "rb"), 'lxml')
                    #response = open(file_name, "rb")
                    #print(f"response {response}")
                    #return response
                    found = True
                    #break
            if not found:
                print(f'\nURL [{url}] \nERRO: [{e}]\n')

            return None

    def download_data1(self, url):
        '''
        Realizar a requisição HTTP e retornar o conteúdo
        '''

        try:
            if "Linux" in platform.system():
                service = Service(executable_path="./geckodriver-linux")
            elif "Windows" in platform.system():
                service = Service(executable_path="./geckodriver.exe")
            else:
                service = Service(executable_path="./geckodriver")

            options = Options()
            # options.headless = True
            options.add_argument("--headless")
            #options.add_argument(r"--binary_location C:\Users\darkt\Apps\FirefoxPortable\App\Firefox64")
            # options.add_argument('--binary_location /usr/bin/firefox')
            # options.binary_location=r"/usr/bin/firefox"
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(url) 
            
            table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table-responsive-sm"))).get_attribute("outerHTML")
            f = io.StringIO(table)
            content = pd.read_html(f)[0]

            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acceptCookieButton"]'))).click()

            # pagination_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located(driver.find_element(By.XPATH, "/html/body/app-root/app-theoretical-portfolio/div/div/div/form/div[2]/div/div[0]/div[1]/nav/pagination-controls/pagination-template/ul")))
            pagination_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located(driver.find_element(By.XPATH, "/html/body/app-root")))
            # teste=WebDriverWait(driver, 20).until(EC.visibility_of_element_located(driver.find_element(By.CSS_SELECTOR, "ngx-pagination")))
            # print(teste)
            # pagination_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "ngx-pagination"))
            print(f"pagination_list {pagination_list}")
            pagination_numbers = pagination_list.find_elements(By.TAG_NAME, "a")
            for page_number in pagination_numbers:
                print(f"page_number {page_number}")
                # Click on the pagination number
                # WebDriverWait(driver, 20).until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, "div.backdrop")))
                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable("ngx-pagination")).click()
                # page_number.click()            

                table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table-responsive-sm"))).get_attribute("outerHTML")
                f = io.StringIO(table)
                content = content + pd.read_html(f)[0]

            print(content)

            # elems = driver.find_element(By.cssSelector("table.table-responsive-sm"));
            # #all_href = driver.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            # content = {}
            # for elem in elems:
            #     #if elem.get_attribute('href') not in content and not elem.get_attribute('href').endswith("indexPage/"):
            #     print(f"XXXXXXXXX [{elem}]")
            #     if not elem.get_attribute('href').endswith("indexPage/"):
            #         #print(elem.get_attribute('href'))
            #         content[elem.text.replace(' ','_').replace('-','').replace('.','').replace('ª','')] = elem.get_attribute('href')
            # #print(all_href)
            # driver.quit()
            # response = requests.get()
            # response.raise_for_status()

            
            # if response.content:
            #     soup = BeautifulSoup(response.content, 'html.parser')
            #     btn_download = soup.find('app-root')
            #     print(f"btn_download {btn_download}")
            #     if btn_download and 'href' in btn_download.attrs:
            #         content = f"{self.source_url}/{btn_download['href']}"
            # print(f"\n\ncontent{response.content}")
            # print(f"\n\ncontent{response.json}")
            #print(list(content))
            return content
        except requests.RequestException as e:
            #file_name = url.split("=")[-1]
            file_name = url.split("/")[-1]
            print(f"options[file_name] {options[file_name]}")
            if options and not options[file_name]:
                file_name = f"{options[file_name]}_default.csv"
            elif sub_options and not sub_options[file_name]:
                file_name = f"{sub_options[file_name]}.csv"
            print(f"file_name {file_name}")
            pattern = re.compile(f"{file_name}[^ ]+.csv")
            found = False
            #print(f"pattern {pattern}")
            for fp in os.listdir("src/database/temp_files/"):
                match = pattern.match(fp)
                #print(f"fp {fp} match {match}")
                if match:
                    file_name = f"src/database/temp_files/{str(match.group(0))}"
                    print(f"O CSV correspondente [{file_name}] existe, tamanho [{os.path.getsize(file_name)}]")
                    #response = BeautifulSoup(open(file_name, "rb"), 'lxml')
                    #response = open(file_name, "rb")
                    #print(f"response {response}")
                    #return response
                    found = True
                    #break
            if not found:
                print(f'\nURL [{url}] \nERRO: [{e}]\n')

            return None

    # def get_subopt(self, opt):

    #     '''
    #     Identificar e retornar todas subopções de uma opção
    #     '''

    #     url = f'{self.source_url}/index.php?opcao={opt}' 

    #     print(f"Pegando subopcao {url} {opt}")
    #     content = self.get_content(url)

    #     if content:

    #         soup = BeautifulSoup(content, 'lxml')
    #         return [btn['value'] for btn in soup.find_all('button', class_='btn_sopt')]

    #     return []

    # def get_download_url(self, opt, sub_opt = None):

    #     '''
    #     Identificar e retornar a URL de download do CSV para cada opção e subopção
    #     '''

    #     if sub_opt:
    #         url = f'{self.source_url}/index.php?subopcao={sub_opt}&opcao={opt}'
    #     else:
    #         url = f'{self.source_url}/index.php?opcao={opt}'

    #     print(f"Obtendo a URL de download {opt} {sub_opt}")
    #     content = self.get_content(url)

    #     if content:

    #         soup = BeautifulSoup(content, 'lxml')
    #         btn_download = soup.find('a', class_='footer_content')

    #         if btn_download and 'href' in btn_download.attrs:

    #             return f"{self.source_url}/{btn_download['href']}"

    #     return None

    # def get_all_download_urls(self, options):

    #     '''
    #     Realizar o mapeamento das combinação de opção, subopção e URL de download
    #     '''

    #     result = []
        
    #     for opt in options:
    #         sub_opts = self.get_subopt(opt)
    #         print(f"SUB_OPTS {sub_opts}")
    #         if sub_opts:
    #             for sub_opt in sub_opts:
    #                 download_url = self.get_download_url(opt, sub_opt)
    #                 if download_url:
    #                     result.append({
    #                         'opt': opt,
    #                         'sub_opt': sub_opt,
    #                         'download_url': download_url
    #                     })
    #         else:
    #             download_url = self.get_download_url(opt)
    #             if download_url:
    #                 result.append({
    #                     'opt': opt,
    #                     'sub_opt': None,
    #                     'download_url': download_url
    #                 })
        
    #     return result

    def get_content(self, url):
        '''
        Realizar a requisição HTTP e retornar o conteúdo
        '''

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            file_name = url.split("/")[-1]
            # print(f"options[file_name] {options[file_name]}")
            # if options and not options[file_name]:
            #     file_name = f"{options[file_name]}_default.csv"
            # elif sub_options and not sub_options[file_name]:
            #     file_name = f"{sub_options[file_name]}.csv"
            print(f"file_name {file_name}")
            pattern = re.compile(f"{file_name}[^ ]+.csv")
            found = False
            #print(f"pattern {pattern}")
            for fp in os.listdir("src/database/temp_files/"):
                match = pattern.match(fp)
                #print(f"fp {fp} match {match}")
                if match:
                    file_name = f"src/database/temp_files/{str(match.group(0))}"
                    print(f"O CSV correspondente [{file_name}] existe, tamanho [{os.path.getsize(file_name)}]")
                    found = True
            if not found:
                print(f'\nURL [{url}] \nERRO: [{e}]\n')

            return None

    def download_csv(self, download_url, folder_path, file_name):

        '''
        Realizar o download e escrita do CSV
        '''

        print(f"Baixando {download_url} {folder_path}/{file_name}")
        content = self.download_data1(download_url)

        if content:

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, file_name)

            print(content)
            with open(file_path, 'wb') as file:
    
                file.write(content)

    def run(self):

        #options = {'Producao.csv':'opt_02', 'opt_03':'opt_03', 'Comercio.csv':'opt_04', 'opt_05':'opt_05', 'opt_06':'opt_06'}
        #sub_options = {'ProcessaViniferas.csv':'opt_03_subopt_01', 'ProcessaAmericanas.csv':'opt_03_subopt_02', 'ProcessaMesa.csv':'opt_03_subopt_03', 'ProcessaSemclass.csv':'opt_03_subopt_04', 
        #               'ImpVinhos.csv':'opt_05_subopt_01', 'ImpEspumantes.csv':'opt_05_subopt_02', 'ImpFrescas.csv':'opt_05_subopt_03', 'ImpPassas.csv':'opt_05_subopt_04', 'ImpSuco.csv':'opt_05_subopt_05',
        #               'ExpVinho.csv':'opt_06_subopt_01', 'ExpEspumantes.csv':'opt_06_subopt_02', 'ExpUva.csv':'opt_06_subopt_03', 'ExpSuco.csv':'opt_06_subopt_04'}

        print(f"Baixando os dados da B3 ...")
        data= self.download_data(self.source_url)
        #print(f"{data}\n")

        for d in data:
            # opt = data['opt']
            # sub_opt = data['sub_opt'] if data['sub_opt'] else 'default'
            # download_url = data['download_url']
            if d != "Download":
                print(f"[{d}] [{data[d]}]")
                file_name = f"{d}.csv"
                file_path = './temp_files'
                print(f"Download CSV {d} ...")
                self.download_csv(data[d], file_path, file_name)
                break