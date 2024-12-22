import os 

from scrapper import Scrapper

def run():

    '''
    Execução do scrapper para extracao dos dados
    '''
    
    scraper = Scrapper()

    scraper.run()

if __name__ == '__main__':

    run()
