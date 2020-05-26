import requests as rq
import bs4 as bs4
import re
import time


def download_search_page(itens, busca):
    url = "https://scholar.google.com.br/scholar?start={itens}&q={busca}&hl=pt-BR&as_sdt=0,5"
    urll = url.format(busca=busca, itens=itens)
    response = rq.get(urll)
    
    return response.text


def parse_search_page(page_html):
    parsed = bs4.BeautifulSoup(page_html)

    link_list = []
    link = titulo = citacoes = ano = tipo_arquivo = versao = ""

    ##Todos os elementos que precisamos estão dentro de uma div com class="gs_ri"
    ##Para cada div dessa na página vamos procurar pelos elementos
    main_tag = parsed.find_all("div", attrs={"class": "gs_ri"})
    data = {}
                
    for e in main_tag:
        ##Link e título
        lista_links = e.h3.findAll('a')
        for i in lista_links:
            link = i['href']
            titulo = i.text
        
        #Número de citações
        lista_citacoes = e.find_all("a", attrs={"href":re.compile(r"cites")})
        for i in lista_citacoes:
            citacoes = re.findall(r'[0-9]+', i.text)
        
        ##Ano de publicação
        lista_anos = e.find_all("div", attrs={"class": "gs_a"})
        for i in lista_anos:
            ano = re.findall(r'[0-9]+', i.text)
    
        ##Tipo do arquivo
        lista_tipo_arquivo = e.find_all("span", attrs={"class": "gs_ct1"})
        for i in lista_tipo_arquivo:
            tipo_arquivo = i.text
        
        ##Quantas versões do arquivo
        lista_versoes = e.find_all("a", attrs={"href":re.compile(r"cluster")})
        for i in lista_versoes:
            versao = re.findall(r'[0-9]+', i.text)
        data = {"link": link, "titulo": titulo, "citacoes": citacoes,
                                "ano": ano, "tipo_arquivo": tipo_arquivo, "versao": versao}
        link_list.append(data)

    return link_list
