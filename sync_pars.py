import requests
from bs4 import BeautifulSoup
import time


# exceptions decorator
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            f = func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Handle specific HTTP errors
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')  # Handle connection-related errors
        except requests.exceptions.Timeout:
            print('The request timed out')  # Handle request timeouts
        except requests.exceptions.RequestException as req_err:
            print(f'An error occurred during the request: {req_err}')  # Handle other request-related errors
        except AttributeError:
            print('Could not find a necessary attribute. The structure of the web page might have changed.')
            # Handle missing attributes in BeautifulSoup
        except IndexError:
            print('Could not access the requested index. The content might not be present.')
            # Handle index errors in BeautifulSoup
        except Exception as e:
            print(f'An unexpected error occurred: {e}')  # Handle any other exceptions
        return f
    return wrapper


@error_handler
def get_hands_phone_number(url):
    # for hands post request from browser inspect
    phone_data = [
        {
            "operationName": "handsRuGetCallCenterPhone",
            "query": "query handsRuGetCallCenterPhone {\n  callCenterPhone\n}\n",
            "variables": {}
        }
    ]
    response = requests.post(url + 'graphql/batch', json=phone_data, timeout=5, verify=True)
    response.raise_for_status()
    print(response.status_code, ' ', url)
    phone_number = response.json()[0]["data"]["callCenterPhone"]
    return phone_number


@error_handler
def get_repetitors_phone_numbers(url):
    response = requests.get(url, timeout=5, verify=True)
    response.raise_for_status()
    print(response.status_code, url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_='foot_box box_right phone_box')
    a_tags = tag.find_all('a')
    phones_list = list(tag_a.string for tag_a in a_tags if tag_a.string is not None)
    return phones_list


@error_handler
def get_city_url_dict():
    repetitors_city_url_dict = {}
    response = requests.get('https://repetitors.info/', timeout=5, verify=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_='city_list')

    for a in tag.find_all('a'):
        repetitors_city_url_dict[a.string] = a.get('href')
    return repetitors_city_url_dict


def dict_format(d):
    s = "Town                  Phone\n"
    for town, phones in d.items():
        phones = ['8'+(''.join(c for c in phone if c.isdecimal()))[1:] for phone in phones]
        s += f'{town:20}' + ', '.join(phones) + '\n'
    return s


def work_with_hands():
    # city: url
    hands_dict = {
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
    # get phone numbers from urls
    # city: phones
    for key, value in hands_dict.items():
        hands_dict[key] = get_hands_phone_number(value)

    # clear the line if there is no phone number
    hands_result_numbers_dict = {}
    for key, value in hands_dict.items():
        if value is not None:
            hands_result_numbers_dict[key] = [value]

    # format and write in file actual_hands_numbers.txt
    with open('actual_hands_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(dict_format(hands_result_numbers_dict))


def work_with_repit():
    # city: url
    repetitors_dict = get_city_url_dict()
    # get phone numbers from urls
    # city: phones
    for town, url in repetitors_dict.items():
        repetitors_dict[town] = get_repetitors_phone_numbers(url)

    # format and write in file actual_repetitors_numbers.txt
    with open('actual_repetitors_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(dict_format(repetitors_dict))


if __name__ == "__main__":
    t0 = time.time()
    work_with_hands()
    work_with_repit()
    print('Current execute time: ', round(time.time()-t0, 2))
