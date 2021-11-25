#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

import json
import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime


def extract_dict_ccaa() -> list:
    """
    Function to get Codes and Names from INE CCAA
    :return: json object with 'CODAUTO' and 'NOMBRE'
    """
    # Request to INE CCAA
    url = 'https://www.ine.es/daco/daco42/codmun/cod_ccaa.htm'
    r = requests.get(url)

    # Parse request url
    soup = BeautifulSoup(r.text, 'html.parser')

    # Create empty lists to collect results
    codauto = []
    nombres = []
    dict_ccaa = []

    # Get and iterate over content
    tds = soup.find_all('td')
    for td in tds:
        contains_digit = any(map(str.isdigit, td.contents[0]))
        if contains_digit:
            codauto.append(int(td.contents[0]))
        elif td.contents[0] != '\n':
            nombres.append(td.contents[0])

    if len(codauto) == len(nombres):
        for i in range(0, len(codauto)):
            dict_ccaa.append({'CODAUTO': str(codauto[i]).zfill(2), 'NOMBRE': nombres[i]})

    return dict_ccaa


def extract_dict_provinces() -> list:
    """
    Function to get Codes and Names from INE Provinces
    :return: json object with 'CODPROV' and 'NOMBRE'
    """
    # Request to INE Provinces
    url = 'https://www.ine.es/daco/daco42/codmun/cod_provincia.htm'
    r = requests.get(url)

    # Parse request url
    soup = BeautifulSoup(r.text, 'html.parser')

    # Create empty lists to collect results
    cpros = []
    names = []
    dict_provinces = []

    # Get and iterate over content
    tds = soup.find_all('td')
    for td in tds:
        contains_digit = any(map(str.isdigit, td.contents[0]))
        if contains_digit:
            cpros.append(int(td.contents[0]))
        elif td.contents[0] != '\n':
            names.append(td.contents[0])

    if len(cpros) == len(names):
        for i in range(0, len(cpros)):
            dict_provinces.append({'CPRO': str(cpros[i]).zfill(2), 'NOMBRE': names[i]})

    return dict_provinces


def extract_dict_municipalities() -> list:
    """
    Function to get Codes and Names from INE Provinces
    :return: json object with 'CODAUTO', 'CPRO', 'CMUN', 'DC' and 'NOMBRE'.
    """
    url = 'https://www.ine.es/daco/daco42/codmun/diccionario21.xlsx'
    r = requests.get(url)

    df = pd.read_excel(r.content, header=1, dtype='str')
    df = df.rename(columns={"NOMBRE ": "NOMBRE"})

    dict_municipalities = json.loads(df.to_json(orient='records'))

    return dict_municipalities


def extract_dict_metadata() -> list:
    """
    Function to get Description and Dates
    :return: json object with 'title', 'description', 'current_data', and 'published_data'.
    """
    dict_metadata = {}
    dict_metadata['title'] = 'Relación de municipios y sus códigos'
    dict_metadata['collections'] = ['ccaa', 'provinces', 'municipalities']

    # Request to 'Relación de municipios y sus códigos por provincias. Últimos datos'
    url = 'https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990'
    r = requests.get(url)

    # Parse request url
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get and iterate over content to get description
    description = ''
    ps = soup.find_all('p')

    for p in soup.find_all('p'):
        text_parts = p.contents
        for text_part in text_parts:
            try:
                text_part = str(text_part.contents[0])
            except Exception:
                text_part = str(text_part)

            description = description + text_part

    description = description.split('>')[-1]
    dict_metadata['description'] = description

    # Get and iterate to get Dates
    dates = []
    spans = soup.find_all('span')

    for span in spans:
        parts = span.contents
        for part in parts:
            try:
                if '/' in part.contents[0]:
                    dates.append(part.contents[0])
            except Exception:
                var = None

    if datetime.strptime(dates[0], '%d/%m/%Y') < datetime.strptime(dates[1], '%d/%m/%Y'):
        current_data = dates[0]
        published_data = dates[1]
    else:
        current_data = dates[1]
        published_data = dates[0]

    dict_metadata['current_data'] = current_data
    dict_metadata['published_data'] = published_data

    return [dict_metadata]
