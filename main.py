import requests
from bs4 import BeautifulSoup


def get_hands_phone_number(url):
    # for hands post request
    phone_data = [
        {
            "operationName": "handsRuGetCallCenterPhone",
            "query": "query handsRuGetCallCenterPhone {\n  callCenterPhone\n}\n",
            "variables": {}
        }
    ]
    response = requests.post(url + 'graphql/batch', json=phone_data)
    print(response.status_code, ' ', url)
    phone_number = response.json()[0]["data"]["callCenterPhone"]
    return phone_number


def dict_format(d):
    s = "Town                  Phone\n"
    for town, phones in d.items():
        phones = ['8'+(''.join(c for c in phone if c.isdecimal()))[1:] for phone in phones]
        s += f'{town:20}' + ', '.join(phones) + '\n'
    return s


def work_with_hands():
    hands_urls_dict = {
        'Астрахань': 'https://astrahan.hands.ru/', 'Барнаул': 'https://barnaul.hands.ru/',
        'Владикавказ': 'https://alania.hands.ru/', 'Владивосток': 'https://primorie.hands.ru/',
        'Волгоград': 'https://volgograd.hands.ru/', 'Воронеж': 'https://vrn.hands.ru/',
        'Екатеринбург': 'https://ekt.hands.ru/', 'Ижевск': 'https://udmurtia.hands.ru/',
        'Иркутск': 'https://irkutsk.hands.ru/', 'Казань': 'https://kzn.hands.ru/',
        'Красноярск': 'https://krsk.hands.ru/',
        'Калининград': 'https://kaliningrad.hands.ru/', 'Кемерово': 'https://kemerovo.hands.ru/',
        'Киров': 'https://kirov.hands.ru/', 'Краснодар': 'https://ksdr.hands.ru/',
        'Липецк': 'https://lipetsk.hands.ru/',
        'Москва': 'https://hands.ru/', 'Махачкала': 'https://dagestan.hands.ru/',
        'Нижний Новгород': 'https://nnov.hands.ru/', 'Новороссийск': 'https://nrsk.hands.ru/',
        'Новосибирск': 'https://nsk.hands.ru/', 'Набережные Челны': 'https://nch.hands.ru/',
        'Новокузнецк': 'https://nkz.hands.ru/', 'Омск': 'https://omsk.hands.ru/',
        'Оренбург': 'https://orenburg.hands.ru/',
        'Пермь': 'https://prm.hands.ru/', 'Псков': 'https://pskov.hands.ru/', 'Пенза': 'https://penza.hands.ru/',
        'Ростов‑на‑Дону': 'https://rnd.hands.ru/', 'Рязань': 'https://ryazan.hands.ru/',
        'Санкт‑Петербург': 'https://spb.hands.ru/', 'Саранск': 'https://mordovia.hands.ru/',
        'Самара': 'https://smr.hands.ru/', 'Саратов': 'https://saratov.hands.ru/', 'Тюмень': 'https://tyumen.hands.ru/',
        'Тула': 'https://tula.hands.ru/', 'Тверь': 'https://tver.hands.ru/', 'Тольятти': 'https://tolyatti.hands.ru/',
        'Томск': 'https://tomsk.hands.ru/', 'Ульяновск': 'https://ulyanovsk.hands.ru/', 'Уфа': 'https://ufa.hands.ru/',
        'Хабаровск': 'https://habarovsk.hands.ru/', 'Челябинск': 'https://chel.hands.ru/',
        'Ярославль': 'https://yar.hands.ru/'
    }
    # ready dict
    hands_numbers_dict = {'Астрахань': None, 'Барнаул': None, 'Владикавказ': '+78672289505', 'Владивосток': None,
                          'Волгоград': None, 'Воронеж': None, 'Екатеринбург': '+73432267057', 'Ижевск': None,
                          'Иркутск': None, 'Казань': '+78432023887', 'Красноярск': None, 'Калининград': None,
                          'Кемерово': None, 'Киров': None, 'Краснодар': None, 'Липецк': None, 'Москва': '+74951370720',
                          'Махачкала': None, 'Нижний Новгород': None, 'Новороссийск': None, 'Новосибирск': None,
                          'Набережные Челны': None, 'Новокузнецк': None, 'Омск': '+73812994031', 'Оренбург': None,
                          'Пермь': None, 'Псков': None, 'Пенза': None, 'Ростов‑на‑Дону': None, 'Рязань': None,
                          'Санкт‑Петербург': '+78122133129', 'Саранск': None, 'Самара': '+78462150448', 'Саратов': None,
                          'Тюмень': '+73452569723', 'Тула': None, 'Тверь': None, 'Тольятти': None, 'Томск': None,
                          'Ульяновск': None, 'Уфа': None, 'Хабаровск': None, 'Челябинск': None, 'Ярославль': None}
    # get phone numbers from urls
    # uncomment if you want to reload database
    """
    for key, value in hands_urls_dict.items():
        hands_numbers_dict[key] = get_hands_phone_number(value)
    """

    # format dict
    hands_result_numbers_dict = {}
    for key, value in hands_numbers_dict.items():
        if value is not None:
            hands_result_numbers_dict[key] = [value]

    with open('actual_hands_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(dict_format(hands_result_numbers_dict))


def work_with_repit():
    repetitors_urls_dict = {}
    response = requests.get('https://repetitors.info/')
    soup = BeautifulSoup(response.text, 'html.parser')

    tag = soup.find(class_='city_list')

    # get dict of town: url
    for a in tag.find_all('a'):
        repetitors_urls_dict[a.string] = a.get('href')

    # ready dict
    repetitors_result_numbers_dict = {'Адыгея': ['8 (800) 555-56-76'], 'Алтай': ['8 (800) 555-56-76'],
                                      'Амурская область': ['8 (800) 555-56-76'],
                                      'Архангельск': ['8 (800) 555-56-76'], 'Астрахань': ['8 (800) 555-56-76'],
                                      'Барнаул': ['8 (800) 555-56-76'],
                                      'Белгород': ['8 (800) 555-56-76'],
                                      'Брянск': ['8 (483) 236-56-50', '8 (800) 555-56-76'],
                                      'Бурятия': ['8 (800) 555-56-76'], 'Великий Новгород': ['8 (800) 555-56-76'],
                                      'Владимир': ['8 (800) 555-56-76'],
                                      'Волгоград': ['8 (844) 243-74-75', '8 (800) 555-56-76'],
                                      'Вологда': ['8 (800) 555-56-76'],
                                      'Воронеж': ['8 (473) 202-56-76', '8 (800) 555-56-76'],
                                      'Дагестан': ['8 (800) 555-56-76'],
                                      'Еврейская АО': ['8 (800) 555-56-76'],
                                      'Екатеринбург': ['8 (343) 317-56-76', '8 (800) 555-56-76'],
                                      'Забайкальский край': ['8 (800) 555-56-76'], 'Иваново': ['8 (800) 555-56-76'],
                                      'Ингушетия': ['8 (800) 555-56-76'],
                                      'Иркутск': ['8 (800) 555-56-76'], 'Кабардино-Балкария': ['8 (800) 555-56-76'],
                                      'Казань': ['8 (843) 211-56-76', '8 (800) 555-56-76'],
                                      'Калининград': ['8 (800) 555-56-76'],
                                      'Калмыкия': ['8 (800) 555-56-76'], 'Калуга': ['8 (800) 555-56-76'],
                                      'Камчатский край': ['8 (800) 555-56-76'],
                                      'Карачаево-Черкесия': ['8 (800) 555-56-76'], 'Карелия': ['8 (800) 555-56-76'],
                                      'Кемерово': ['8 (800) 555-56-76'],
                                      'Киров': ['8 (800) 555-56-76'], 'Коми': ['8 (800) 555-56-76'],
                                      'Кострома': ['8 (800) 555-56-76'],
                                      'Краснодар': ['8 (800) 555-56-76'],
                                      'Красноярск': ['8 (391) 216-56-67', '8 (800) 555-56-76'],
                                      'Крым': ['8 (800) 555-56-76'],
                                      'Курган': ['8 (352) 222-56-75', '8 (800) 555-56-76'],
                                      'Курск': ['8 (471) 225-02-30', '8 (800) 555-56-76'],
                                      'Липецк': ['8 (474) 255-63-76', '8 (800) 555-56-76'],
                                      'Магадан': ['8 (800) 555-56-76'], 'Марий Эл': ['8 (800) 555-56-76'],
                                      'Мордовия': ['8 (800) 555-56-76'],
                                      'Москва': ['8 (495) 540-56-76'], 'Мурманск': ['8 (800) 555-56-76'],
                                      'Ненецкий АО': ['8 (800) 555-56-76'],
                                      'Нижний Новгород': ['8 (831) 218-56-67', '8 (800) 555-56-76'],
                                      'Новосибирск': ['8 (383) 284-56-76', '8 (800) 555-56-76'],
                                      'Омск': ['8 (3812) 66-56-07', '8 (800) 555-56-76'],
                                      'Орёл': ['8 (800) 555-56-76'],
                                      'Оренбург': ['8 (353) 266-56-71', '8 (800) 555-56-76'],
                                      'Пенза': ['8 (841) 299-56-76', '8 (800) 555-56-76'],
                                      'Пермь': ['8 (342) 215-67-80'],
                                      'Приморский край': ['8 (800) 555-56-76'], 'Псков': ['8 (800) 555-56-76'],
                                      'Ростов-на-Дону': ['8 (863) 307-56-76', '8 (800) 555-56-76'],
                                      'Рязань': ['8 (491) 251-56-72', '8 (800) 555-56-76'],
                                      'Самара': ['8 (846) 203-56-76', '8 (800) 555-56-76'],
                                      'Санкт-Петербург': ['8 (812) 385-53-15'],
                                      'Саратов': ['8 (845) 265-05-60'], 'Северная Осетия': ['8 (800) 555-56-76'],
                                      'Смоленск': ['8 (800) 555-56-76'],
                                      'Сочи': ['8 (495) 540-56-76'], 'Ставрополь': ['8 (800) 555-56-76'],
                                      'Тамбов': ['8 (800) 555-56-76'],
                                      'Тверь': ['8 (482) 273-56-67', '8 (800) 555-56-76'],
                                      'Тольятти': ['8 (495) 540-56-76'],
                                      'Томск': ['8 (382) 299-56-68', '8 (800) 555-56-76'],
                                      'Тула': ['8 (487) 252-32-31', '8 (800) 555-56-76'],
                                      'Тыва': ['8 (800) 555-56-76'], 'Тюмень': ['8 (800) 555-56-76'],
                                      'Удмуртия': ['8 (800) 555-56-76'],
                                      'Ульяновск': ['8 (842) 230-56-78', '8 (800) 555-56-76'],
                                      'Уфа': ['8 (800) 555-56-76'],
                                      'Хабаровск': ['8 (800) 555-56-76'], 'Хакасия': ['8 (800) 555-56-76'],
                                      'Ханты-Мансийский АО': ['8 (800) 555-56-76'],
                                      'Челябинск': ['8 (351) 218-56-76', '8 (800) 555-56-76'],
                                      'Чечня': ['8 (800) 555-56-76'],
                                      'Чувашия': ['8 (835) 220-56-76'], 'Чукотский АО': ['8 (800) 555-56-76'],
                                      'Южно-Сахалинск': ['8 (800) 555-56-76'],
                                      'Якутия': ['8 (800) 555-56-76'], 'Ямало-Ненецкий АО': ['8 (800) 555-56-76'],
                                      'Ярославль': ['8 (485) 228-56-75', '8 (800) 555-56-76']}
    # get phone numbers from urls
    # uncomment if you want to reload database
    """
    for town, url in repetitors_urls_dict.items():
        response = requests.get(url)
        print(response.status_code, url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tag = soup.find(class_='foot_box box_right phone_box')
        a_tags = tag.find_all('a')
        repetitors_result_numbers_dict[town] = list(tag_a.string for tag_a in a_tags if tag_a.string is not None)
    """

    with open('actual_repetitors_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(dict_format(repetitors_result_numbers_dict))


if __name__ == "__main__":
    work_with_hands()
    work_with_repit()
