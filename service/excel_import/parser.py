import datetime
import re
import urllib.parse

import requests
from geopy.distance import geodesic
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium_stealth import stealth
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)


stealth(driver,
        languages=["en-US", "en", 'ru'],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

CIAN_URL = "https://www.cian.ru/cat.php"
MAPBOX_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

mapbox = {
    'access_token': '',
    'limit': 1,
    'bbox': '37,55.45,38,56',
}

params_cian = {
    "deal_type": "sale",
    "engine_version": 2,
    "offer_type": "flat",
    "region": 1,
    'house_material%5B0%5D': None,
    'only_flat': 1,
}

header = {
    'User-Agent': '',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': "en-GB,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
    # 'cache-control': 'max-age=0',
    # 'if-none-match': 'W/"23cdca-LL20nen8Y/RAHtqQ7afgDkPlSj0"',
    # 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': "Windows",
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-user': '?1',
    # 'upgrade-insecure-requests': '1',
    # 'cookie': '_CIAN_GK=113ab85d-4baf-48a9-9d89-10cb21f88526; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; uxfb_usertype=searcher; _ga=GA1.2.1521098410.1666793294; tmr_lvid=5d67c6253e3541774bd896587834ed0c; tmr_lvidTS=1644083631271; _ym_uid=1657007208865946641; _ym_d=1666793294; afUserId=4684da3e-6b42-4c89-8d01-58cb3614b362-p; AF_SYNC=1666793294793; _cc_id=3d70e297552a244ffa03e45b18f89307; panoramaId_expiry=1667398094773; panoramaId=5914f51ecde0a7258967bade963316d539388da0532cd4954e90f625f3ad64c7; cookie_agreement_accepted=1; _gcl_au=1.1.1552798899.1666793430; uxs_uid=40d45460-5538-11ed-924b-ad76d085ce37; _hjSessionUser_2021803=eyJpZCI6Ijk5YWU3YWIzLWRjNjUtNTk1Ny04YzBjLTBmOWU0Nzc4ZjFhYiIsImNyZWF0ZWQiOjE2NjY3OTM1NjEyNzUsImV4aXN0aW5nIjpmYWxzZX0=; DMIR_AUTH=LgQl0RM1IK%2F6ZaLjwj2%2FvSO8Yl78drxCl2gQfm5VjkOacT9Q7wbUe%2Fakgn3ZCGj0oMMC9Cp5OWxmBzILA4VC8we22lNM5QuiukPoi5RAAdhh7S2uB%2B9Cn2%2Br3G49U%2F8Rd2122eQ7bSqhkWZw%2BgUbwwkY7lKae8s0Oa7V5jOuWeY%3D; cian_ruid=96788218; _gid=GA1.2.758572866.1667294964; _ym_isad=1; _gpVisits={"isFirstVisitDomain":true,"todayD":"Tue%20Nov%2001%202022","idContainer":"10002511"}; session_region_id=1; session_main_town_region_id=1; adb=1; cookieUserID=96788218; sopr_session=c2b2b13ffb194f01; _ym_visorc=b; tmr_detect=1%7C1667316813491; _gp10002511={"hits":18,"vc":1,"ac":1,"a6":1}; __cf_bm=7EauF.8.bnAevDhxTFuYuTfDXCsV6nviIO8WWp6wsRE-1667317274-0-AUk0mKuzS1UOg34hUBYfaTPJgdjOt62vJINpGF86OFkdBXO0ojwEINBPwSTHrOOGIivvt2tOdPDPDihQ+EJk2gI=; tmr_reqNum=224',
}

from_xlsx_to_cian = {
    '1': "room1",
    '2': "room2",
    '3': "room3",
    '4': "room4",
    'студия': "room9",
}

check = ["г. Москва, ул. Ватутина, д. 11", "2", "Современное жилье", "22", "Панель", "7", "85.0" "15.0" "1", "11",
         "Муниципальный ремонт"]

def create_anfl(link_address):
    trans = {
        'общая': 'total_area',
        'этаж': 'floor',
        'отделка': 'condition',
        'кухня': 'kitchen_area',
    }
    fl = {}
    link = link_address[0]
    address = link_address[1]
    driver.get(link)
    time.sleep(2)
    soup = bs(driver.page_source, 'html.parser')
    if soup.find('span', 'a10a3f92e9--underground_time--iOoHy'):
        fl['minutes_metro_walk'] = re.search(r'([0-9]+)', soup.find('span', 'a10a3f92e9--underground_time--iOoHy').text).group()
    else:
        fl['minutes_metro_walk'] = 15
    price = soup.find('span', itemprop='price').get('content').replace(' ', '')
    fl['price'] = re.search(r'[0-9,.]*', price).group()
    print(price)
    data = soup.find_all('div', 'a10a3f92e9--info--PZznE')
    fl['have_balcony'] = True if 'балкон/лоджия' in map(lambda x: x.text.lower(),
                                                        soup.find_all('span', 'a10a3f92e9--name--x7_lt')
                                                        ) else False
    attributes = list(map(lambda x: x.text.lower(), soup.find_all('li', 'a10a3f92e9--value--Y34zN')))
    for i in data:
        print(i)
        field_type = i.find('div', 'a10a3f92e9--info-title--JWtIm').text.lower()
        field_value = i.find('div', 'a10a3f92e9--info-value--bm3DC').text
        if field_type in trans:
            print(field_type, field_value)
            if field_type == 'общая' or field_type == 'кухня':
                field_value = float(re.search(r'[0-9,.]*', field_value).group().replace(',', '.'))
            elif field_type == 'этаж':
                res = re.findall(r'[0-9]*', field_value)
                cur_floor, last_floor = res[0], res[1]
                if cur_floor == last_floor:
                    flr = 'last'
                elif int(cur_floor) == 1:
                    flr = 'first'
                else:
                    flr = 'mid'
                field_value = flr
            elif field_type == 'отделка':
                field_value = 'муниципальный ремонт'
            fl[trans[field_type]] = field_value
            print(fl)
    if 'condition' not in fl:
        if 'косметический' in attributes or 'без ремонта' in attributes:
            rs_condition = 'без отделки'
        elif 'евроремонт' or 'дизайнерский ремонт':
            rs_condition = 'современная отделка'
        else:
            rs_condition = 'муниципальная ремонт'
        fl['condition'] = rs_condition
    if 'kitchen_area' not in fl:
        fl['kitchen_area'] = 10
    fl['location'] = address
    return fl


def get_coord(address, loop = 0):
    global  mapbox
    print(MAPBOX_URL + f'{address}.json?' + '&'.join(f'{i}={mapbox[i]}' for i in mapbox))
    req = requests.get(MAPBOX_URL + f'{address}.json?' + '&'.join(f'{i}={mapbox[i]}' for i in mapbox))
    match req.status_code:
        case 200:
            d = req.json()
            print(d)
            center = d['features'][0]['center']
            coord = (center[0], center[1])
            return coord
        case _:
            print(req.status_code, req.text)



def update_params_cian(segment, wall_material):
    print(segment, wall_material)
    cur_time = datetime.datetime.now().year - 2
    if segment == 'новостройка':
        params_cian['min_house_year'] = cur_time
    elif segment == 'современное жилье':
        params_cian['min_house_year'] = 1989
        params_cian['max_house_year'] = cur_time
    elif segment == 'старый жилой фонд':
        params_cian['max_house_year'] = 1989
    if wall_material == 'кирпич':
        params_cian[r'house_material%5B0%5D'] = 1
    elif wall_material == 'панель':
        params_cian[r'house_material%5B0%5D'] = 3
    elif wall_material == 'монолит':
        params_cian[r'house_material%5B0%5D'] = 2


def parse(references: list, req_pool, current_app) -> list:
    global mapbox
    mapbox['access_token'] = current_app.config.get('MAPBOX_API')
    return parse_cian(references, req_pool)


def parse_cian(references: list, req_pool) -> list:
    references_analogues = []
    segment = req_pool.segment
    wall_material = req_pool.wall_material
    floor_quantity = req_pool.floor_quantity
    location = req_pool.location
    print(location.find('д.'))
    print(location[:location.find('д.')])
    reference_coord = get_coord(location[:location.find('д.')])
    page = 1
    min_dist = 1500000000
    for flat in references:
        analogue_flats = []
        params_cian[from_xlsx_to_cian[flat.room_quantity.name]] = 1
        update_params_cian(segment.name, wall_material.name)
        while len(analogue_flats) < 3:

            current_cian_url = CIAN_URL + "?" + '&'.join([f'{i}={params_cian[i]}' for i in params_cian])
            print(floor_quantity, params_cian, current_cian_url + f'&page={page}')
            driver.get(current_cian_url + f'&page={page}')
            time.sleep(1)
            soup = bs(driver.page_source, 'html.parser')
            if soup.find('h3', '_93444fe79c--banner-text-bold--u9Hpv'):
                break
            flats = soup.find_all('div', '_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy')
            print(flats)
            for fl in flats:
                link = fl.find('a', '_93444fe79c--link--eoxce').get('href')
                address = ', '.join(map(lambda x: x.text, fl.find_all('a', '_93444fe79c--link--NQlVc')))
                print(link, address, )
                analogue_coord = get_coord(address)
                print(geodesic(reference_coord, analogue_coord).meters, reference_coord, analogue_coord)
                if geodesic(reference_coord, analogue_coord).meters <= 1500:
                    analogue_flats.append((link, address))
                min_dist = min(min_dist, geodesic(reference_coord, analogue_coord).meters)
            print('YOOOOOOOOOOOOOO:', min_dist, f'REF COORD: {reference_coord}')
            page += 1
            print(analogue_flats)
        res_anfl = []
        for i in analogue_flats:
            res_anfl.append(create_anfl(i))
        references_analogues.append(res_anfl)
    return references_analogues



    driver.quit()
    print(analogue_flats)

def parse_avito():
    pass

# create_anfl(('https://www.cian.ru/sale/flat/278316490/', 'Москва, ЗАО, р-н Фили-Давыдково, ул. Герасима Курина, 20'))
# create_anfl(('https://www.cian.ru/sale/flat/276827883/', 'Москва, ЗАО, р-н Очаково-Матвеевское, м. Аминьевская, Озерная улица, 4к1'))
# create_anfl(('https://www.cian.ru/sale/flat/279466244/', 'Москва, ЗАО, р-н Фили-Давыдково, м. Пионерская, Кастанаевская улица, 43К4'))
# create_anfl(('https://www.cian.ru/sale/flat/278847841/', 'Москва, ЗАО, р-н Очаково-Матвеевское, м. Славянский бульвар, Веерная улица, 1К4'))