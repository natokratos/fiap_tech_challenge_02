from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import re

class Scrapper:

    def __init__(self):
        
        self.source_url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

    def download_data(self):
        '''
        Realizar a requisição HTTP e retornar o conteúdo
        '''

        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            driver.get(self.source_url)            
            elems = driver.find_elements(By.XPATH,  "//*[contains(@href, 'indexPage/')]")
            #all_href = driver.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            content = []
            for elem in elems:
                if elem.get_attribute('href') not in content and not elem.get_attribute('href').endswith("indexPage/"):
                    #print(elem.get_attribute('href'))
                    content.append(elem.get_attribute('href'))
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

    def download_csv(self, download_url, folder_path, file_name, options, sub_options):

        '''
        Realizar o download e escrita do CSV
        '''

        print(f"Baixando {download_url} {folder_path} {file_name}")
        content = self.get_content(download_url, options, sub_options)

        if content:

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'wb') as file:
    
                file.write(content)

    def run(self):

        #options = {'Producao.csv':'opt_02', 'opt_03':'opt_03', 'Comercio.csv':'opt_04', 'opt_05':'opt_05', 'opt_06':'opt_06'}
        #sub_options = {'ProcessaViniferas.csv':'opt_03_subopt_01', 'ProcessaAmericanas.csv':'opt_03_subopt_02', 'ProcessaMesa.csv':'opt_03_subopt_03', 'ProcessaSemclass.csv':'opt_03_subopt_04', 
        #               'ImpVinhos.csv':'opt_05_subopt_01', 'ImpEspumantes.csv':'opt_05_subopt_02', 'ImpFrescas.csv':'opt_05_subopt_03', 'ImpPassas.csv':'opt_05_subopt_04', 'ImpSuco.csv':'opt_05_subopt_05',
        #               'ExpVinho.csv':'opt_06_subopt_01', 'ExpEspumantes.csv':'opt_06_subopt_02', 'ExpUva.csv':'opt_06_subopt_03', 'ExpSuco.csv':'opt_06_subopt_04'}

        print(f"Baixando os dados da B3 ...")
        data= self.download_data()
        #print(f"{data}\n")

        for data in data:
            print(data)
            # opt = data['opt']
            # sub_opt = data['sub_opt'] if data['sub_opt'] else 'default'
            # download_url = data['download_url']
            # file_name = f"{opt}_{sub_opt}.csv"
            # file_path = 'src/database/temp_files'
            # print(f"Download CSV {download_url} ...")
            self.download_csv(data, file_path, file_name, options, sub_options)