import requests
import json
import datetime
from collections import Counter

friends = 'friends.get'
token = '85ab7071ea2f29b754f1b3cef324018ff3d82d9c1b127e1d006597e9e67f3cf4acf0c4c3a4648ea4c17ee'
year = datetime.datetime.now().year
age_gate = []


def get_url(metod, id, token):
    url = 'https://api.vk.com/method/{}?user_id={}&fields=bdate&access_token={}&v=5.102'.format(metod, id, token)
    return url


def calc_age(URL):
    age_status = []
    url = requests.get(URL)
    if url.status_code == 200:
        items = url.json().get('response').get('items')
        for item in items:
            if item.get('bdate') != None:
                if len(item.get('bdate')) >= 8:
                    if len(item.get('bdate')) == 8:
                        age_status.append(year - int(item.get('bdate')[4:]))
                    elif len(item.get('bdate')) == 9:
                        age_status.append(year - int(item.get('bdate')[5:]))
                    else:
                        age_status.append(year - int(item.get('bdate')[6:]))
        return age_status
    else:
        raise requests.HTTPError


if __name__ == "__main__":
    id = input('Введите id пользовотеля ')
    cont = Counter(calc_age(get_url(friends, id, token)))
    for sort in sorted(cont.items(), key=lambda x: x[1], reverse=True):
        age_gate.append(sort)

    print(age_gate)
