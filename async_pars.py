from bs4 import BeautifulSoup
import aiohttp
import asyncio
import sys
import time


def error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError:
            print('HTTP Client Error occurred')
            # Handle aiohttp errors
        except AttributeError:
            print('Could not find a necessary attribute. The structure of the web page might have changed.')
            # Handle missing attributes in BeautifulSoup
        except IndexError:
            print('Could not access the requested index. The content might not be present.')
            # Handle index errors in BeautifulSoup
        except Exception as e:
            print(f'An unexpected error occurred: {e}')  # Handle any other exceptions
        # return f
    return wrapper


async def dict_format(d):
    s = "Town                  Phone\n"
    for town, phones in d.items():
        phones = ['8'+(''.join(c for c in phone if c.isdecimal()))[1:] for phone in phones]
        s += f'{town:20}' + ', '.join(phones) + '\n'
    return s


@error_handler
async def get_repetitors_phone_numbers(session, url):
    async with session.get(url) as response:
        print(response.status, ' ', url)
        soup = BeautifulSoup(await response.text(), 'html.parser')
        tag = soup.find(class_='foot_box box_right phone_box')
        a_tags = tag.find_all('a')
        phones_list = list(tag_a.string for tag_a in a_tags if tag_a.string is not None)
        return phones_list


@error_handler
async def get_hands_phone_number(session, url):
    # for hands post request from browser inspect
    phone_data = [
        {
            "operationName": "handsRuGetCallCenterPhone",
            "query": "query handsRuGetCallCenterPhone {\n  callCenterPhone\n}\n",
            "variables": {}
        }
    ]
    async with session.post(url+'graphql/batch', json=phone_data) as response:
        print(response.status, ' ', url)
        phone_number = await response.json()
        return phone_number[0]["data"]["callCenterPhone"]


@error_handler
async def get_city_url_dict(session):
    async with session.get('https://repetitors.info/') as response:
        repetitors_city_url_dict = {}
        soup = BeautifulSoup(await response.text(), 'html.parser')
        tag = soup.find(class_='city_list')
        for a in tag.find_all('a'):
            repetitors_city_url_dict[a.string] = a.get('href')
        return repetitors_city_url_dict


@error_handler
async def work_with_hands(session):
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
    tasks = []
    for url in hands_dict.values():
        task = asyncio.create_task(get_hands_phone_number(session, url))
        tasks.append(task)
    list_of_numbers = await asyncio.gather(*tasks)

    # city: phones
    i = 0
    for key in hands_dict.keys():
        hands_dict[key] = list_of_numbers[i]
        i += 1

    # clear the line if there is no phone number
    hands_result_numbers_dict = {}
    for key, value in hands_dict.items():
        if value is not None:
            hands_result_numbers_dict[key] = [value]

    # format and write in file actual_hands_numbers.txt
    with open('actual_hands_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(await dict_format(hands_result_numbers_dict))

    return hands_result_numbers_dict

@error_handler
async def work_with_repit(session):
    # city: url
    repetitors_dict = await get_city_url_dict(session)
    # get phone numbers from urls
    tasks = []
    for url in repetitors_dict.values():
        task = asyncio.create_task(get_repetitors_phone_numbers(session, url))
        tasks.append(task)
    list_of_numbers = await asyncio.gather(*tasks)

    # city: phones
    i = 0
    for town in repetitors_dict.keys():
        repetitors_dict[town] = list_of_numbers[i]
        i += 1

    # format and write in file actual_repetitors_numbers.txt
    with open('actual_repetitors_numbers.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(await dict_format(repetitors_dict))

    return repetitors_dict


@error_handler
async def main():
    async with aiohttp.ClientSession() as session:
        t0 = time.time()
        await work_with_hands(session)
        await work_with_repit(session)
        print('Current execute time: ', round(time.time()-t0, 2))

if __name__ == '__main__':
    # for "RuntimeError: Event loop is closed" issue on Windows
    # https://github.com/aio-libs/aiohttp/issues/4324?ysclid=ltdruls192596785616
    if sys.version_info[:2] == (3, 7):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(2.0))
    finally:
        loop.close()

