from bs4 import BeautifulSoup as bs
import requests
import re
import json

def _parser_item_hh(item):
    vacancy_date = {}

    # vacancy_name
    vacancy_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()

    vacancy_date['vacancy_name'] = vacancy_name

    # company_name
    company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').getText()

    vacancy_date['company_name'] = company_name

    # city
    city = item.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()

    vacancy_date['city'] = city

    # metro station
    metro_station = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).findChild()
    if not metro_station:
        metro_station = None
    else:
        metro_station = metro_station.getText()

    vacancy_date['metro_station'] = metro_station

    # salary
    salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\u202f', u'')
        salary = re.split(r'\s|-', salary)
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[2])

        salary_currency = salary[-1]
    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency

    # link
    is_ad = item.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_controls'}).getText()
    vacancy_link = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
    if is_ad != 'ОткликнутьсяРеклама':
        vacancy_link = vacancy_link.split('?')[0]
    vacancy_date['vacancy_link'] = vacancy_link


    # site
    vacancy_date['site'] = 'hh.ru'
    return vacancy_date

def _parser_hh(vacancy):
    global last_page
    vacancy_date = []

    params = {
        'text': vacancy,
        'search_field': 'name',
        'items_on_page': '100',
        'page': ''
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.3.757 Yowser/2.5 Safari/537.36'}

    url = 'https://hh.ru/search/vacancy'

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        parsed_url = bs(response.text, 'html.parser')
        if not parsed_url:
            last_page = '1'
        else:
            last_page = int(parsed_url.find_all('a', {'data-qa': 'pager-page'})[-1].getText())

    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(url, params=params, headers=headers)

        if html.ok:
            parsed_url = bs(response.text, 'html.parser')

            vacancy_items = parsed_url.find('div', {'data-qa': 'vacancy-serp__results'}) \
                .find_all('div', {'class': 'vacancy-serp-item'})

            for item in vacancy_items:
                vacancy_date.append(_parser_item_hh(item))
    return vacancy_date





vacancy = 'Python'
vacancy_date = []
vacancy_date.extend(_parser_hh(vacancy))

with open('data2.json', 'w') as f:
    json.dump(vacancy_date, f)
