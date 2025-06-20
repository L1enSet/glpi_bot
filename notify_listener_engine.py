import requests
import json
from requests.auth import HTTPBasicAuth


def create_profile(glpi_data, tg_id, tg_name, login, _pass, dst_url):
    url = dst_url
    headers = {
        'ContentType': 'application/json',

        }
    auth = HTTPBasicAuth(login, _pass)
    data = glpi_data
    data['tg_id'] = tg_id
    data['tg_name'] = tg_name
    data['is_active'] = 'true'

    response = requests.post(url=url, headers=headers, data=data, auth=auth)
    print(response.text)
    
    result = {}
    result['status'] = response.status_code
    if response.status_code == 201:
        result['data'] = json.loads(response.text)
    elif response.status_code == 400:
        result['data'] = json.loads(response.text)
        result['error'] = "Duplicate user"
    print(data)
    return result
